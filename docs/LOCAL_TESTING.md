# Local Testing

## Setup

1. Create Python virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Verify config.json exists and OpenAI API key file path is reachable.

## Run Application

```powershell
python app.py
```

Open http://127.0.0.1:5000 in browser.

## Test Flows

### Manual Transaction Entry
1. Navigate to "Add Transaction"
2. Enter: amount, merchant, category, date, note
3. Click "Add"
4. Check Dashboard to see transaction listed

### CSV Upload
1. Create sample CSV with header: `date,merchant,amount,category,note`
2. Add rows of sample data
3. Navigate to "Upload CSV"
4. Select file and click "Upload"
5. Check Dashboard

### Receipt Upload
1. Prepare receipt image (PNG, JPG, JPEG, WebP)
2. Navigate to "Upload Receipt"
3. Select image, click "Upload"
4. Placeholder parsing saves transaction
5. Check Dashboard

### Insights Generation
1. Add several transactions via any method
2. Navigate to "Insights"
3. View behavioral summary (either OpenAI if API key configured, or heuristic fallback)

## Run Tests

```powershell
pytest -v
```

Expected: all tests pass.

## Check Logs

```
logs/app.log
```

View timestamped error messages and info logs.

## Preflight Errors

If app shows startup errors:
1. Check config.json exists
2. Check OpenAI API key file path (from config.json) exists
3. Check data, uploads, logs folders can be created
4. View logs/app.log for details

## Stop Server

Press `Ctrl+C` in terminal running `python app.py`.
