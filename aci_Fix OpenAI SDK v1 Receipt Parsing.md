# ACI — Fix OpenAI SDK v1 Receipt Parsing
# VERSION: 2.1
# TARGET: GitHub Copilot
# FEATURE: OpenAI SDK Modernization Fix
# PROJECT: Financial Intelligence App / Financial Nebula Node

---

# PROJECT LOCAL PATH

C:\Users\tim\Documents\business_related\The_AI_Guy\nebula\other_app_created_with_nebula\financial_app

---

# PRIMARY OBJECTIVE

Fix the OpenAI receipt parsing feature.

Current issue:
The app reaches the OpenAI integration path, but fails because the code uses deprecated OpenAI Python SDK syntax:

openai.ChatCompletion

This is no longer supported in openai>=1.0.0.

Do NOT downgrade or pin openai==0.28.

Update the code to use the modern OpenAI Python SDK client syntax.

---

# REQUIRED BRANCH

Create and work from:

feature/fix-openai-sdk-v1-receipt-parsing

Do not modify deployable directly.

---

# CURRENT VALIDATED STATE

The following already works:

- Flask app runs locally
- UI loads
- receipt upload route works
- dashboard updates
- transaction persistence works
- fallback behavior works
- GitHub Actions works
- deployable branch governance works
- OpenAI integration path is reached

Current failure category:

OPENAI_API_ERROR

Root cause:

Deprecated OpenAI SDK call syntax.

---

# REQUIRED FIX

Update the OpenAI receipt parsing service.

Likely file:

app/services/openai_receipt_service.py

Replace any usage of:

openai.ChatCompletion

with modern OpenAI SDK syntax:

from openai import OpenAI

client = OpenAI(api_key=api_key)

Use the modern client call pattern for a vision-capable model.

---

# REQUIRED RECEIPT IMAGE FLOW

The service must:

1. Receive uploaded image path
2. Read image bytes
3. Base64 encode image
4. Send image to OpenAI using modern SDK
5. Request structured JSON extraction
6. Parse response
7. Return normalized receipt/transaction data

---

# REQUIRED EXTRACTED FIELDS

Return this structure when possible:

{
  "merchant": "",
  "date": "",
  "total": 0.0,
  "category": "",
  "items": [],
  "confidence": "",
  "raw_summary": ""
}

---

# REQUIRED PROMPT BEHAVIOR

Ask OpenAI to extract receipt data as strict JSON.

The model should identify:

- merchant
- date
- total
- category
- line items if visible
- short behavioral summary

If information is missing, return safe defaults.

---

# REQUIRED FALLBACK BEHAVIOR

If OpenAI fails:

- app must not crash
- user must see readable fallback note
- transaction should still be created if upload succeeded
- error should be logged to logs/app.log
- error category should remain OPENAI_API_ERROR

---

# REQUIRED TESTING

Add or update tests so CI does NOT require a real OpenAI API call.

CI must use mock behavior.

Tests should validate:

- service imports successfully
- API key loader works with a mocked path
- parser handles mock OpenAI response
- parser handles OpenAI failure gracefully
- app route still works

---

# LOCAL MANUAL TEST

After patching, run:

python app.py

Open:

http://127.0.0.1:5000

Then upload a real receipt.

Expected success:

- merchant is no longer filename
- amount is no longer $0.00
- category is not unknown/uncategorized if detectable
- note shows AI parsed or OpenAI parsed result
- dashboard reflects parsed transaction

---

# CI/CD REQUIREMENTS

GitHub Actions must pass.

CI must NOT call OpenAI live.

Use mocks for OpenAI-related tests.

---

# DOCUMENTATION UPDATE

Update:

docs/PCAP_openai_receipt_parsing.md

Add section:

## SDK Compatibility Fix

Include:

- original error
- root cause
- fix strategy
- modern SDK direction
- why downgrade was rejected
- testing notes

Update:

docs/GOVERNANCE.md

Add governance:

## OpenAI SDK Compatibility Governance

Rule:
Do not pin legacy SDK versions to avoid fixing code unless explicitly approved.

Prefer modern SDK-compatible code.

---

# COMMIT MESSAGE

Use meaningful commit message:

Fix OpenAI SDK v1 receipt parsing integration

---

# SUCCESS CONDITIONS

This feature fix is successful when:

- deprecated openai.ChatCompletion usage is removed
- modern OpenAI client syntax is used
- app reaches OpenAI without SDK syntax failure
- receipt parsing returns structured data or clean fallback
- local receipt upload test works
- logs are clean/readable
- tests pass
- GitHub Actions passes
- feature branch is ready for review

---

END OF ACI