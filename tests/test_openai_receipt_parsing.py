import pytest
import os
import json
from unittest.mock import patch, MagicMock
from app.services.openai_receipt_service import OpenAIReceiptParsingService


@pytest.fixture
def service():
    """Create receipt parsing service instance."""
    return OpenAIReceiptParsingService()


@pytest.fixture
def sample_receipt_path(tmp_path):
    """Create temporary receipt image file."""
    img_file = tmp_path / "test_receipt.png"
    # Create minimal PNG bytes (1x1 transparent PNG)
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    img_file.write_bytes(png_bytes)
    return str(img_file)


def test_service_initialization(service):
    """Test service initializes without error."""
    assert service is not None
    assert service.model is not None


def test_api_key_loading(service):
    """Test API key loading from config."""
    # Service should attempt to load API key
    # May be None if file doesn't exist (expected in CI)
    assert service.api_key is None or isinstance(service.api_key, str)


def test_fallback_transaction(service, sample_receipt_path):
    """Test fallback transaction generation."""
    fallback = service._fallback_transaction(sample_receipt_path, "Test error")
    assert fallback['merchant'] == os.path.basename(sample_receipt_path)
    assert fallback['amount'] == '0.00'
    assert fallback['category'] == 'uncategorized'
    assert 'fallback' in fallback['note'].lower()


def test_parse_receipt_image_missing_file(service):
    """Test parsing non-existent file returns fallback."""
    result = service.parse_receipt_image('/nonexistent/file.png')
    assert result['amount'] == '0.00'
    assert result['category'] == 'uncategorized'


def test_parse_receipt_image_file_exists(service, sample_receipt_path):
    """Test parsing with valid file path."""
    # Without API key, should return fallback
    result = service.parse_receipt_image(sample_receipt_path)
    assert isinstance(result, dict)
    assert 'merchant' in result
    assert 'amount' in result
    assert 'category' in result
    assert 'date' in result


@patch('openai.OpenAI')
def test_openai_api_call(mock_openai_class, service, sample_receipt_path):
    """Test OpenAI API call with mocked response (modern SDK v1.0+)."""
    # Mock successful OpenAI response using modern SDK structure
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Mock the response object structure for modern SDK
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        'merchant': 'Test Store',
        'amount': '42.50',
        'date': '2025-05-21',
        'category': 'groceries'
    })
    mock_client.chat.completions.create.return_value = mock_response
    
    # Set dummy API key to trigger API call
    service.api_key = 'sk-dummy-test-key'
    service._client = None  # Reset client to trigger lazy load
    
    result = service.parse_receipt_image(sample_receipt_path)
    # Will either call API (if mocked) or return fallback
    assert isinstance(result, dict)
    assert 'merchant' in result
    assert 'amount' in result


@patch('openai.OpenAI')
def test_openai_json_response_valid(mock_openai_class, service, sample_receipt_path):
    """Test valid JSON response is parsed correctly."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        'merchant': 'Test Store',
        'total': 42.5,
        'date': '2025-05-21',
        'category': 'groceries',
        'items': [],
        'confidence': 'high',
        'raw_summary': 'Parsed receipt successfully.'
    })
    mock_client.chat.completions.create.return_value = mock_response
    service.api_key = 'sk-dummy-test-key'
    service._client = None

    result = service.parse_receipt_image(sample_receipt_path)
    assert result['merchant'] == 'Test Store'
    assert float(result['amount']) == 42.5
    assert result['date'] == '2025-05-21'
    assert result['category'] == 'groceries'
    assert 'Parsed receipt successfully.' in result['note']


@patch('openai.OpenAI')
def test_openai_json_response_with_code_fence(mock_openai_class, service, sample_receipt_path):
    """Test JSON response wrapped in markdown code fences is parsed correctly."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    raw_json = json.dumps({
        'merchant': 'Fence Store',
        'total': 13.75,
        'date': '2025-06-01',
        'category': 'food',
        'items': [],
        'confidence': 'medium',
        'raw_summary': 'Parsed from fenced JSON.'
    })
    mock_response = MagicMock()
    mock_response.choices[0].message.content = f"```json\n{raw_json}\n```"
    mock_client.chat.completions.create.return_value = mock_response
    service.api_key = 'sk-dummy-test-key'
    service._client = None

    result = service.parse_receipt_image(sample_receipt_path)
    assert result['merchant'] == 'Fence Store'
    assert float(result['amount']) == 13.75
    assert result['category'] == 'food'


@patch('openai.OpenAI')
def test_openai_empty_response_fallback(mock_openai_class, service, sample_receipt_path):
    """Test empty OpenAI response triggers fallback."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = ''
    mock_client.chat.completions.create.return_value = mock_response
    service.api_key = 'sk-dummy-test-key'
    service._client = None

    result = service.parse_receipt_image(sample_receipt_path)
    assert result['amount'] == '0.00'
    assert result['category'] == 'uncategorized'
    assert 'fallback' in result['note'].lower()


@patch('openai.OpenAI')
def test_openai_malformed_json_response_fallback(mock_openai_class, service, sample_receipt_path):
    """Test malformed JSON response triggers fallback."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{merchant: "Bad Store", total: 22.00,}'
    mock_client.chat.completions.create.return_value = mock_response
    service.api_key = 'sk-dummy-test-key'
    service._client = None

    result = service.parse_receipt_image(sample_receipt_path)
    assert result['amount'] == '0.00'
    assert result['category'] == 'uncategorized'
    assert 'fallback' in result['note'].lower()


def test_category_normalization(service):
    """Test category field normalization."""
    fallback = service._fallback_transaction('/tmp/test.jpg')
    assert fallback['category'] in ['groceries', 'food', 'fuel', 'healthcare', 
                                     'entertainment', 'utilities', 'other', 'uncategorized']


def test_amount_coercion(service):
    """Test amount field is string and numeric."""
    fallback = service._fallback_transaction('/tmp/test.jpg')
    amount = fallback['amount']
    assert isinstance(amount, str)
    # Should be parseable as float
    float(amount)
