# Financial Nebula Node — MVP

Behavior-aware financial operational intelligence.

## Quick Start

1. **Setup:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure:**
   - Ensure `config.json` exists with your settings
   - Place your OpenAI API key file at the path specified in `config.json`
   - Default: `C:\Users\tim\Desktop\openai_key_for_financial_app.txt`

3. **Run:**
   ```powershell
   python app.py
   ```
   Then open: http://127.0.0.1:5000

## Features

- Receipt image upload (PNG, JPG, JPEG, WebP)
- Manual transaction entry
- CSV transaction upload
- Transaction normalization
- Behavioral insight generation via OpenAI
- Simple goal correlation
- Local JSON persistence

## Configuration

See `config.json` for:
- Flask secret key
- OpenAI API key file path
- OpenAI model selection
- Upload folder location
- Upload file size limits

## Logs

Application logs are written to `logs/app.log` with timestamped entries.

Error categories: CONFIG_ERROR, API_KEY_ERROR, FILE_UPLOAD_ERROR, CSV_PARSE_ERROR, OPENAI_API_ERROR, STORAGE_ERROR, VALIDATION_ERROR

## Testing

```powershell
pytest -v
```

## Docs

- [PCAP.md](docs/PCAP.md) - Project architecture
- [LOCAL_TESTING.md](docs/LOCAL_TESTING.md) - Testing workflows
- [GOVERNANCE.md](docs/GOVERNANCE.md) - Branch governance

## Tech Stack

- Python 3.12+
- Flask
- OpenAI API
- Local JSON storage
