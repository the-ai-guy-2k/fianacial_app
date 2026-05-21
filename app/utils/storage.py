import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
TX_FILE = os.path.join(DATA_DIR, 'transactions.json')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.json')


def load_transactions():
    if not os.path.exists(TX_FILE):
        return []
    try:
        with open(TX_FILE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return []


def save_transactions(txs):
    try:
        with open(TX_FILE, 'w', encoding='utf-8') as fh:
            json.dump(txs, fh, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def get_default_goals():
    """Return default goals for MVP testing."""
    return [
        {
            'id': 'goal_emergency_fund',
            'name': 'Emergency Fund Goal',
            'target': 5000.0,
            'description': 'Build emergency fund'
        }
    ]
