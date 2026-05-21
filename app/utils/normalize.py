import uuid
from datetime import datetime


def normalize_transaction(raw):
    """Normalize raw transaction dict into standard format.
    
    Handles:
    - amount: coerce to float, format as string
    - merchant/payee: extract and trim
    - category: default to 'uncategorized'
    - date: ISO format or current time
    - note: optional
    - id: generate UUID if missing
    """
    tx = {}
    tx['id'] = raw.get('id') if isinstance(raw, dict) and raw.get('id') else str(uuid.uuid4())
    
    # amount: coerce to float string
    amt = raw.get('amount') if isinstance(raw, dict) else None
    try:
        amt_val = float(str(amt).replace('$', '').replace(',', ''))
    except Exception:
        amt_val = 0.0
    tx['amount'] = f"{amt_val:.2f}"
    
    # merchant/payee
    tx['merchant'] = (raw.get('merchant') or raw.get('payee') or '').strip()
    
    # category: default to uncategorized
    tx['category'] = (raw.get('category') or '').strip() or 'uncategorized'
    
    # date: use provided or current
    tx['date'] = raw.get('date') or datetime.utcnow().isoformat()
    
    # note: optional
    tx['note'] = raw.get('note') or ''
    
    return tx
