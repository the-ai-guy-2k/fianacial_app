# PCAP — OpenAI Receipt Parsing Feature

## Feature Purpose

Enable real OpenAI-powered receipt parsing to extract structured financial transaction data from receipt images uploaded by users.

### Problem Solved
- Previous version used placeholder parsing
- New version extracts merchant, amount, date, category from receipt images via OpenAI vision API
- Enables automation of transaction entry from physical/digital receipts

### Value Delivered
- Users can upload receipt images instead of manually entering transaction details
- OpenAI extracts structured data (merchant, amount, date, category)
- Transactions automatically normalized and saved
- Behavioral insights generated from parsed transactions

---

## Architecture Overview

### Component: OpenAI Receipt Parsing Service

Location: `app/services/openai_receipt_service.py`

**Responsibilities:**
- Load OpenAI API key from config file path
- Read receipt image from disk
- Encode image to base64
- Call OpenAI ChatCompletion API with vision
- Parse JSON response
- Validate extracted fields
- Return normalized transaction dict
- Handle errors gracefully with fallback parsing

**Key Methods:**
- `__init__()`: Load API key, initialize client
- `parse_receipt_image(file_path)`: Main parsing workflow
- `_get_client()`: Lazy-load OpenAI client
- `_fallback_transaction()`: Return minimal transaction on failure

### Workflow Flow

```
User Upload Receipt Image
    ↓
Flask Route: /upload_receipt
    ↓
Validate: format, size, file permissions
    ↓
Save locally to uploads/ folder
    ↓
OpenAI Receipt Parsing Service
    ├─ Load API key from config file
    ├─ Read image file
    ├─ Encode to base64
    ├─ Call OpenAI ChatCompletion + Vision API
    ├─ Parse JSON response
    └─ Return: {merchant, amount, date, category, note}
    ↓
Normalize Transaction
    ├─ Generate UUID
    ├─ Coerce amount to float
    ├─ Set defaults (category, date)
    └─ Return normalized transaction object
    ↓
Save to data/transactions.json
    ↓
Redirect to Dashboard
    ↓
Display parsed merchant and amount in flash message
```

---

## Dependencies

### Python Packages
- `openai>=0.27.0` — OpenAI API client
- Already in requirements.txt

### Configuration
- `config.json` required values:
  - `openai.api_key_file`: File path to OpenAI API key
  - `openai.model`: Model to use (e.g., `gpt-4-mini`)
  - `upload.max_size_mb`: Max upload size (e.g., 10)
  - `upload.allowed_receipt_formats`: Array of allowed formats

### External Service
- OpenAI API (ChatCompletion with vision capability)
- Requires valid API key with vision model access

---

## OpenAI Integration Details

### Model
- **Model**: `gpt-4-mini` (configurable in config.json)
- **Capability**: Vision (image understanding)

### API Call Format
```
POST /v1/chat/completions
Message: {
    "role": "user",
    "content": [
        {"type": "text", "text": "Extract receipt data..."},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
    ]
}
```

### Expected Response
```json
{
    "merchant": "Whole Foods Market",
    "amount": "47.82",
    "date": "2025-05-21",
    "category": "groceries",
    "line_items": [...]
}
```

### Prompt Engineering
The service sends a structured prompt asking OpenAI to:
1. Extract merchant name
2. Extract total amount
3. Extract transaction date (ISO format)
4. Infer category (food, groceries, fuel, etc.)
5. Optionally extract line items
6. Return as valid JSON only

---

## Configuration Requirements

### config.json Settings
```json
{
  "openai": {
    "api_key_file": "C:\\Users\\tim\\Desktop\\openai_key_for_financial_app.txt",
    "model": "gpt-4-mini"
  },
  "upload": {
    "max_size_mb": 10,
    "allowed_receipt_formats": ["png", "jpg", "jpeg", "webp"]
  }
}
```

### API Key File
- **Location**: Path specified in `config.json`
- **Format**: Plain text, single line
- **Content**: OpenAI API key (sk-...)
- **Permissions**: File must be readable by Flask process

---

## Error Classification & Logging

### Error Categories
- `API_KEY_ERROR`: API key missing, invalid, or unreadable
- `FILE_UPLOAD_ERROR`: File format/size validation, read failures
- `OPENAI_API_ERROR`: OpenAI API call failures
- `VALIDATION_ERROR`: JSON parsing or data validation failures
- `CONFIG_ERROR`: Config missing or malformed

### Logging
- All errors logged to `logs/app.log` with timestamps
- Format: `[timestamp] - [logger] - [level] - [category] [message] | Error: [details]`

### Example Log Entries
```
2025-05-21 12:34:56,789 - financial_app - ERROR - [API_KEY_ERROR] OpenAI API key file not found: C:\Users\tim\Desktop\openai_key_for_financial_app.txt
2025-05-21 12:34:57,012 - financial_app - INFO - Receipt parsed successfully: Whole Foods Market
2025-05-21 12:35:01,345 - financial_app - ERROR - [OPENAI_API_ERROR] OpenAI API call failed | Error: (401, 'Unauthorized')
```

---

## Fallback & Resilience

### Graceful Failure Handling
If OpenAI parsing fails, the system:
1. Logs error with category and details
2. Returns fallback transaction object
3. Continues transaction creation with fallback data
4. Displays error message to user
5. Does NOT crash the application

### Fallback Transaction
```python
{
    'merchant': '<filename>',
    'amount': '0.00',
    'date': '',
    'category': 'uncategorized',
    'note': 'Fallback: [error reason]'
}
```

User still sees transaction created; they can manually edit if needed.

---

## Testing Workflow

### Local Testing Steps

1. **Setup**
   ```powershell
   python app.py
   ```

2. **Navigate to Upload Receipt**
   - http://127.0.0.1:5000/upload_receipt

3. **Upload Real Receipt**
   - Select PNG/JPG/JPEG/WebP image of receipt
   - Click "Upload"

4. **Verify Parsing**
   - Check flash message for parsed merchant and amount
   - Navigate to Dashboard
   - Verify transaction appears with:
     - Extracted merchant name
     - Extracted amount
     - Extracted date (if present)
     - Inferred category

5. **Verify Insights**
   - Navigate to /insights
   - Verify insight generation works with parsed data

6. **Check Logs**
   - Review `logs/app.log`
   - Verify success and error messages

### Error Scenario Testing

**Scenario 1: Missing API Key**
- Temporarily rename `.openai_api_key_for_financial_app.txt`
- Upload receipt
- Expected: Fallback parsing, error logged, transaction created with fallback data

**Scenario 2: Invalid Image**
- Upload non-image file (TXT, PDF)
- Expected: Format validation error before upload

**Scenario 3: Large File**
- Upload image > 10MB
- Expected: Size validation error before upload

**Scenario 4: Blank Receipt**
- Upload completely blank image
- Expected: OpenAI returns empty/minimal fields, fallback used

### Unit Tests

Located: `tests/test_openai_receipt_parsing.py`

Tests validate:
- API key loading from config
- Image file validation (format, size)
- Base64 encoding
- OpenAI client initialization
- Fallback parsing on API failure
- Error logging

---

## Troubleshooting

### Issue: "OpenAI API key file not found"
**Cause**: File path in config.json doesn't exist
**Solution**: 
1. Check config.json `openai.api_key_file` path
2. Verify file exists at that path
3. Verify Flask process has read permissions

### Issue: "Failed to initialize OpenAI client"
**Cause**: openai package not installed or API key format invalid
**Solution**:
1. Run `pip install -q openai`
2. Verify API key file contains valid key (starts with `sk-`)
3. Check logs for detailed error

### Issue: "OpenAI API call failed"
**Cause**: API key invalid, quota exceeded, or API change
**Solution**:
1. Verify API key is current and valid
2. Check OpenAI account has available credits
3. Verify model name in config matches available model
4. Check OpenAI status page for outages

### Issue: "Received empty response from OpenAI"
**Cause**: Model doesn't support vision or malformed request
**Solution**:
1. Verify model supports vision (gpt-4-mini, gpt-4-vision, etc.)
2. Check image encoding is base64
3. Verify image format is supported (JPEG, PNG, GIF, WebP)

### Issue: "Transaction created but merchant is empty"
**Cause**: Receipt OCR unclear or image quality too low
**Solution**:
1. User can manually edit transaction after creation
2. Upload clearer receipt image
3. Check logs for OpenAI parsing details

---

## Expected Outputs

### Success Case
```
User uploads receipt image
→ [INFO] Receipt uploaded: receipt_20250521.jpg
→ [INFO] Receipt parsed successfully: Whole Foods Market
→ Flash message: "Receipt parsed: Whole Foods Market - $47.82"
→ Dashboard shows transaction:
  - ID: [uuid]
  - Date: 2025-05-21
  - Merchant: Whole Foods Market
  - Category: groceries
  - Amount: $47.82
  - Note: Parsed from receipt: receipt_20250521.jpg
```

### Partial Failure Case
```
User uploads receipt image
→ [ERROR] [OPENAI_API_ERROR] OpenAI API call failed | Error: ...
→ [INFO] Receipt parsed successfully: receipt_20250521.jpg (fallback)
→ Flash message: "Receipt parsed: receipt_20250521.jpg - $0.00"
→ Dashboard shows transaction with fallback data
→ User can manually edit merchant, amount, category
```

### Full Failure Case
```
User uploads receipt image
→ [ERROR] [API_KEY_ERROR] OpenAI API key file not found
→ Flash message: "Receipt uploaded but failed to save transaction"
→ Dashboard shown; transaction NOT created
→ Error details in logs/app.log
```

---

## Deployment Impact

### Breaking Changes
- None. Feature is additive.

### New Requirements
- Valid OpenAI API key with vision capability
- Config.json updated with API key file path
- API key file placed at specified path

### Performance Impact
- Each receipt upload now makes 1 API call to OpenAI
- Typical latency: 2-5 seconds per receipt
- API cost: ~$0.01-0.05 per receipt (depends on image size and model)

### Rollback Considerations
- If OpenAI API becomes unavailable:
  - Fallback parsing still works
  - App continues operational
  - Users get fallback transactions
  - No data loss

- If feature needs to be disabled:
  1. Revert route to use old `ai.parse_receipt()` placeholder
  2. No data migration needed
  3. Existing transactions unaffected

---

## Git Branch & Governance

### Branch
- **Name**: `feature/openai-receipt-parsing`
- **Base**: `deployable`
- **Status**: Active development

### Commits
- Initial feature implementation
- Test coverage additions
- Documentation

### Merge Criteria
- ✅ All tests pass locally
- ✅ GitHub Actions CI passes
- ✅ Receipt parsing verified operationally
- ✅ No breaking changes
- ✅ Error handling validated

### Post-Merge
- Merge into `deployable` branch
- Tag as stable release
- Update main README if needed

---

## Future Enhancements

1. **Receipt OCR Fallback**: Add pytesseract fallback if OpenAI fails
2. **Receipt Line Items**: Extract and display individual items
3. **Receipt Image Gallery**: Store and display receipt thumbnails
4. **Receipt Categorization AI**: Use behavioral insights to suggest categories
5. **Expense Reports**: Generate expense reports from parsed receipts
6. **Receipt Audit Trail**: Track parsing confidence and manual edits

---

## Success Metrics

Feature successful when:
- ✅ Receipt images reach OpenAI API
- ✅ Merchant extracted accurately
- ✅ Amount extracted accurately
- ✅ Date extracted accurately
- ✅ Category inferred logically
- ✅ Transactions saved to dashboard
- ✅ Behavioral insights generated
- ✅ Errors logged with timestamps
- ✅ Fallback parsing operational
- ✅ CI/CD pipeline passes
- ✅ No regressions in existing features
- ✅ Merge to deployable complete

