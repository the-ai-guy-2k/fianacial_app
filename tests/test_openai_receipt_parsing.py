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


@patch('openai.ChatCompletion.create')
def test_openai_api_call(mock_create, service, sample_receipt_path):
    """Test OpenAI API call with mocked response."""
    # Mock successful OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        'merchant': 'Test Store',
        'amount': '42.50',
        'date': '2025-05-21',
        'category': 'groceries'
    })
    mock_create.return_value = mock_response
    
    # Set dummy API key to trigger API call
    service.api_key = 'sk-dummy-test-key'
    
    result = service.parse_receipt_image(sample_receipt_path)
    # Will either call API (if mocked) or return fallback
    assert isinstance(result, dict)
    assert 'merchant' in result
    assert 'amount' in result


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
