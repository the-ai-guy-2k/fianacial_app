# PCAP — Project Control and Architecture Plan

## Operational Purpose

Financial Nebula Node MVP is a local-first, behavior-aware financial operational intelligence system that normalizes financial data, identifies patterns, generates insights, and correlates transactions with goals.

## Architecture

### Core Components

1. **Flask Web App** (`app/__init__.py`, `app.py`)
   - Local development server on http://127.0.0.1:5000
   - Blueprint-based routing

2. **Routes** (`app/routes/main.py`)
   - Dashboard: transaction overview + goals
   - /upload_receipt: receipt image upload (placeholder AI parsing)
   - /upload_csv: CSV bulk import
   - /add_transaction: manual transaction entry
   - /insights: behavioral insights generation

3. **Services** (`app/services/openai_service.py`)
   - Receipt parsing (placeholder)
   - Behavioral insight generation
   - Rules-first + AI-enhanced architecture

4. **Utilities**
   - `config_manager.py`: Config loading from config.json
   - `preflight.py`: Startup validation
   - `logging_service.py`: Timestamped error classification
   - `storage.py`: JSON file persistence
   - `normalize.py`: Transaction normalization

5. **Storage**
   - `data/transactions.json`: Transaction records
   - `logs/app.log`: Timestamped application logs

### Workflows

- **Receipt Upload**: Upload image → AI parsing (placeholder) → Normalize → Save to JSON
- **CSV Import**: Upload CSV → Parse rows → Normalize → Deduplicate → Save
- **Manual Entry**: Form submission → Normalize → Save
- **Insights**: Load transactions → Call OpenAI → Return summary

### Startup Preflight

On app boot, validate:
- config.json exists
- OpenAI API key file exists and readable
- data/uploads/logs folders exist or can be created
- Flask secret key configured

### Error Classification

- `CONFIG_ERROR`: Config file/Flask secret issues
- `API_KEY_ERROR`: OpenAI key file missing/invalid
- `FILE_UPLOAD_ERROR`: Upload size/format violations
- `CSV_PARSE_ERROR`: CSV parsing issues
- `OPENAI_API_ERROR`: API call failures
- `STORAGE_ERROR`: Folder/file write failures
- `VALIDATION_ERROR`: Data validation issues

## Branch Strategy

- Feature branches for development
- Local testing before push
- GitHub Actions CI validates syntax, imports, tests
- Merge to `deployable` branch after CI pass
- `deployable` = stable operational state

## Deployment Strategy

Local-first MVP: no cloud, no containers, no DB. Single-file deployable branch artifact.

## Testing Workflow

- Unit tests in `tests/` with pytest
- CI runs full test suite
- Lightweight validation: syntax check, import test, config test

## MVP Boundary

**In scope:**
- Flask local app
- Receipt + CSV + manual entry
- Transaction normalization
- Behavioral insights
- Local JSON storage
- Simple goal correlation
- Error logging

**Out of scope:**
- Database
- Authentication
- Docker/containers
- Cloud deployment
- Advanced frontend
- Mobile apps

## Future Roadmap

1. Enhanced receipt OCR/vision API parsing
2. Goal tracking dashboard
3. Recurring transaction detection
4. Budget alerts
5. Export to formats (PDF, Excel)
6. Multi-user support with authentication
7. Cloud sync option
