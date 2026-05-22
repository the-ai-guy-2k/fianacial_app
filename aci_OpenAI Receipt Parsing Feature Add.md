# ACI — OpenAI Receipt Parsing Feature Add
# VERSION: 2.0
# TARGET: GitHub Copilot
# FEATURE: Real OpenAI Receipt Parsing
# PROJECT: Financial Intelligence App / Financial Nebula Node

---

# PROJECT LOCAL PATH

C:\Users\tim\Documents\business_related\The_AI_Guy\nebula\other_app_created_with_nebula\financial_app

---

# REMOTE REPO

https://github.com/the-ai-guy-2k/fianacial_app.git

---

# PRIMARY OBJECTIVE

Add REAL OpenAI receipt parsing to the existing operational MVP.

Current state:
- receipt upload works
- local persistence works
- dashboard works
- CI/CD works
- deployable governance works

Current limitation:
receipt parsing is still placeholder logic.

This feature add replaces placeholder parsing with:
# real OpenAI-powered receipt extraction.

---

# REQUIRED BRANCH WORKFLOW

Create and use:

feature/openai-receipt-parsing

This feature branch must:
- pass local testing
- pass GitHub Actions
- merge into deployable only after validation

---

# REQUIRED FEATURE PCAP

Create:

docs/PCAP_openai_receipt_parsing.md

Include:
- feature purpose
- architecture flow
- dependencies
- OpenAI workflow
- config requirements
- testing steps
- troubleshooting guidance
- expected outputs
- rollback considerations
- deployment impact

---

# REQUIRED CONFIG SUPPORT

Use existing config.json.

Required values:

- OpenAI API key file path
- OpenAI model
- upload folder
- Flask secret fallback

Current API key file path:

C:\Users\tim\Desktop\openai_key_for_financial_app.txt

---

# OPENAI API KEY LOADING

The app must:

- read API key from file path
- strip whitespace/newlines
- validate key exists
- fail gracefully if missing

Do NOT hardcode API key.

Do NOT commit secrets.

---

# REQUIRED OPENAI FEATURE FLOW

New workflow:

receipt upload
→ save locally
→ send image to OpenAI
→ receive structured extraction
→ normalize transaction
→ save transaction
→ display parsed transaction
→ generate behavioral insight

---

# REQUIRED RECEIPT EXTRACTION FIELDS

Attempt to extract:

- merchant
- total amount
- transaction date
- category
- line items if possible

Fallback gracefully if fields missing.

---

# OPENAI MODEL

Use:

gpt-4.1-mini

---

# REQUIRED SERVICE LAYER

Create isolated OpenAI receipt parsing service.

Recommended location:

app/services/openai_receipt_service.py

The service should:
- load config
- load API key
- call OpenAI API
- parse response
- classify errors
- return normalized structure

---

# REQUIRED ERROR CLASSIFICATION

Support:

- API_KEY_ERROR
- OPENAI_API_ERROR
- VALIDATION_ERROR
- FILE_UPLOAD_ERROR
- CONFIG_ERROR

Log all errors to:

logs/app.log

Use timestamped entries.

---

# REQUIRED FALLBACK BEHAVIOR

If OpenAI parsing fails:
- app must NOT crash
- upload must remain operational
- fallback transaction may still be created
- user should receive readable operational error message

---

# REQUIRED TESTING

Validate:
- API key loads successfully
- OpenAI request succeeds
- parsed values populate dashboard
- malformed receipt handled gracefully
- missing API key handled gracefully
- invalid image handled gracefully

---

# REQUIRED LOCAL TEST FLOW

Expected local workflow:

python app.py

Open:
http://127.0.0.1:5000

Then:
- upload real receipt
- verify parsed merchant
- verify parsed amount
- verify parsed date
- verify insight generation
- verify dashboard updates

---

# REQUIRED CI/CD SUPPORT

Update GitHub Actions if needed.

CI/CD should:
- validate imports
- validate tests
- NOT call live OpenAI API during CI

Use mock testing where appropriate.

---

# REQUIRED GIT GOVERNANCE

Copilot must:
- create feature branch
- commit changes with meaningful commit messages
- push feature branch
- preserve deployable branch stability

Do NOT merge into deployable until:
- local tests pass
- GitHub Actions pass
- OpenAI parsing verified operationally

---

# IMPORTANT EXECUTION RULES

Do NOT:
- rebuild the entire app
- introduce databases
- add Docker
- add cloud deployment
- add auth systems
- overengineer

This is:
# feature operationalization phase

Focus on:
- real OpenAI parsing
- operational reliability
- graceful failure handling
- clean workflow integration

---

# SUCCESS CONDITIONS

Feature is successful when:
- uploaded receipt reaches OpenAI
- merchant extracted correctly
- amount extracted correctly
- transaction saved correctly
- dashboard reflects parsed data
- insight generation works
- logs created correctly
- CI/CD passes
- feature branch stable
- deployable merge ready

---

END OF ACI