import os
import json
from app.utils.config_manager import config
from app.utils.logging_service import ErrorCategory, log_error, log_info

class OpenAIService:
    """Minimal OpenAI service abstraction for MVP.

    Loads API key from path specified in config.json.
    Methods are safe no-ops when API key or `openai` package is missing.
    """

    def __init__(self):
        self.api_key = None
        self.model = config.get('openai.model', 'gpt-4-mini')
        api_key_file = config.get('openai.api_key_file')
        
        if api_key_file and os.path.exists(api_key_file):
            try:
                with open(api_key_file, 'r', encoding='utf-8') as fh:
                    self.api_key = fh.read().strip()
                log_info(f"OpenAI API key loaded from config path")
            except Exception as e:
                log_error(ErrorCategory.API_KEY_ERROR, "Failed to load OpenAI API key", e)

        self._client = None

    def _has_client(self):
        if self._client is not None:
            return True
        try:
            import openai
            if self.api_key:
                openai.api_key = self.api_key
            self._client = openai
            return True
        except Exception:
            return False

    def parse_receipt(self, file_path_or_bytes):
        """Parse receipt image and return transaction dict.
        
        In MVP, this is a placeholder. In future, sends image to OpenAI vision API.
        """
        if self._has_client() and self.api_key:
            try:
                # Placeholder: in future, use vision API
                return {
                    'amount': '0.00',
                    'merchant': os.path.basename(str(file_path_or_bytes)),
                    'category': 'unknown',
                    'date': '',
                    'note': 'Parsed from receipt (placeholder)'
                }
            except Exception as e:
                log_error(ErrorCategory.OPENAI_API_ERROR, "Receipt parsing failed", e)
        
        # Fallback
        return {
            'amount': '0.00',
            'merchant': os.path.basename(str(file_path_or_bytes)),
            'category': 'unknown',
            'date': '',
            'note': 'Receipt file uploaded (AI parsing unavailable)'
        }

    def generate_insights(self, transactions):
        """Generate behavioral insights from transactions using OpenAI or heuristics."""
        if self._has_client() and self.api_key:
            try:
                prompt = f"""Generate brief behavioral financial insights from these transactions (max 200 words):
{json.dumps(transactions)[:4000]}

Focus on:
- spending patterns
- behavioral observations
- actionable insights"""
                
                resp = self._client.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                insight = resp.choices[0].message.content.strip()
                log_info("Behavioral insights generated via OpenAI")
                return insight
            except Exception as e:
                log_error(ErrorCategory.OPENAI_API_ERROR, "Insight generation failed", e)
        
        # Simple heuristic fallback
        total = 0.0
        count = 0
        categories = {}
        for t in transactions:
            try:
                amt = float(t.get('amount') or 0)
                total += amt
                count += 1
                cat = t.get('category', 'uncategorized')
                categories[cat] = categories.get(cat, 0) + 1
            except Exception:
                continue
        
        avg = (total / count) if count else 0
        top_cat = max(categories, key=categories.get) if categories else 'none'
        
        insight = f"""Financial Overview (heuristic):
- Transactions: {count}
- Total: ${total:.2f}
- Average: ${avg:.2f}
- Top category: {top_cat}

Note: Full insights require OpenAI API access."""
        return insight
