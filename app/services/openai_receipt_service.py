import os
import base64
import json
from app.utils.config_manager import config
from app.utils.logging_service import ErrorCategory, log_error, log_info


class OpenAIReceiptParsingService:
    """Dedicated service for OpenAI-powered receipt parsing.
    
    Workflow:
    1. Load image from file
    2. Encode to base64
    3. Send to OpenAI vision API
    4. Parse structured response
    5. Return normalized transaction dict
    """

    def __init__(self):
        self.api_key = None
        self.model = config.get('openai.model', 'gpt-4-mini')
        api_key_file = config.get('openai.api_key_file')
        self._client = None
        self._load_api_key(api_key_file)

    def _load_api_key(self, api_key_file):
        """Load and validate OpenAI API key from file."""
        if not api_key_file:
            log_error(ErrorCategory.API_KEY_ERROR, "OpenAI API key file path not in config")
            return
        
        if not os.path.exists(api_key_file):
            log_error(ErrorCategory.API_KEY_ERROR, f"OpenAI API key file not found: {api_key_file}")
            return
        
        try:
            with open(api_key_file, 'r', encoding='utf-8') as fh:
                self.api_key = fh.read().strip()
            if not self.api_key:
                log_error(ErrorCategory.API_KEY_ERROR, "OpenAI API key file is empty")
                self.api_key = None
            else:
                log_info("OpenAI API key loaded successfully")
        except Exception as e:
            log_error(ErrorCategory.API_KEY_ERROR, "Failed to read OpenAI API key file", e)

    def _get_client(self):
        """Lazy-load OpenAI client."""
        if self._client is not None:
            return self._client
        
        if not self.api_key:
            log_error(ErrorCategory.API_KEY_ERROR, "Cannot initialize OpenAI client: API key not available")
            return None
        
        try:
            import openai
            openai.api_key = self.api_key
            self._client = openai
            return self._client
        except Exception as e:
            log_error(ErrorCategory.OPENAI_API_ERROR, "Failed to initialize OpenAI client", e)
            return None

    def parse_receipt_image(self, file_path):
        """Parse receipt image using OpenAI vision API.
        
        Args:
            file_path: Path to receipt image file
            
        Returns:
            dict with parsed transaction fields:
            {
                'merchant': str,
                'amount': str (float as string),
                'date': str (ISO format or empty),
                'category': str,
                'note': str
            }
        """
        if not os.path.exists(file_path):
            msg = log_error(ErrorCategory.FILE_UPLOAD_ERROR, f"Receipt file not found: {file_path}")
            return self._fallback_transaction(file_path, msg)
        
        # Check file size
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            max_size = config.get('upload.max_size_mb', 10)
            if file_size_mb > max_size:
                msg = log_error(ErrorCategory.FILE_UPLOAD_ERROR, f"Receipt file too large: {file_size_mb:.1f}MB")
                return self._fallback_transaction(file_path, msg)
        except Exception as e:
            log_error(ErrorCategory.FILE_UPLOAD_ERROR, "Failed to check file size", e)
        
        # Read and encode image
        try:
            with open(file_path, 'rb') as fh:
                image_data = base64.standard_b64encode(fh.read()).decode('utf-8')
        except Exception as e:
            msg = log_error(ErrorCategory.FILE_UPLOAD_ERROR, "Failed to read receipt image", e)
            return self._fallback_transaction(file_path, msg)
        
        # Call OpenAI API
        client = self._get_client()
        if not client:
            msg = "OpenAI API key not configured. Using fallback parsing."
            log_error(ErrorCategory.API_KEY_ERROR, msg)
            return self._fallback_transaction(file_path, msg)
        
        try:
            # Determine image type from filename
            _, ext = os.path.splitext(file_path)
            ext = ext.lower().lstrip('.')
            media_type_map = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'webp': 'image/webp',
                'gif': 'image/gif'
            }
            media_type = media_type_map.get(ext, 'image/jpeg')
            
            # Call OpenAI ChatCompletion with vision
            response = client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this receipt image and extract the following information in JSON format:
{
    "merchant": "store/restaurant name",
    "amount": "total amount as number",
    "date": "transaction date in YYYY-MM-DD format or empty string",
    "category": "inferred category: food, groceries, fuel, healthcare, entertainment, utilities, other",
    "line_items": [{"description": "item", "price": "price"}]
}

Return ONLY valid JSON, no other text. If a field cannot be extracted, use empty string for text fields or 0 for amounts."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{media_type};base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse response
            response_text = response.choices[0].message.content.strip()
            parsed = json.loads(response_text)
            log_info(f"Receipt parsed successfully: {parsed.get('merchant', 'unknown')}")
            
            # Normalize parsed data
            return {
                'merchant': str(parsed.get('merchant', '')).strip(),
                'amount': str(parsed.get('amount', '0.00')).strip(),
                'date': str(parsed.get('date', '')).strip(),
                'category': str(parsed.get('category', 'other')).strip().lower() or 'other',
                'note': f"Parsed from receipt: {os.path.basename(file_path)}"
            }
        
        except json.JSONDecodeError as e:
            msg = log_error(ErrorCategory.VALIDATION_ERROR, "Failed to parse OpenAI response as JSON", e)
            return self._fallback_transaction(file_path, msg)
        
        except Exception as e:
            msg = log_error(ErrorCategory.OPENAI_API_ERROR, "OpenAI API call failed", e)
            return self._fallback_transaction(file_path, msg)

    def _fallback_transaction(self, file_path, error_msg=''):
        """Return minimal fallback transaction when parsing fails."""
        return {
            'merchant': os.path.basename(file_path),
            'amount': '0.00',
            'date': '',
            'category': 'uncategorized',
            'note': f'Fallback: {error_msg}' if error_msg else 'Fallback parsing (API unavailable)'
        }
