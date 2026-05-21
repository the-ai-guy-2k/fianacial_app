# ACI — Financial Nebula Node MVP Rebuild
# VERSION: 1.2
# TARGET: GitHub Copilot
# PROJECT: Financial Intelligence App / Financial Nebula Node

---

# PROJECT LOCAL PATH

C:\Users\tim\Documents\business_related\The_AI_Guy\nebula\other_app_created_with_nebula\financial_app

---

# REMOTE REPO

https://github.com/the-ai-guy-2k/fianacial_app.git

---

# PRIMARY OBJECTIVE

Perform a FULL REBUILD of the Financial Intelligence App MVP as a local-first Flask web application.

The app is NOT a budgeting app.

The app IS:

behavior-aware financial operational intelligence.

Core philosophy:

Most financial problems are behavioral, not mathematical.

---

# REQUIRED MVP FEATURES

Build a working local UI that supports:

- receipt image upload
- manual transaction entry
- CSV transaction upload
- transaction normalization
- behavioral insight generation
- simple goal correlation
- local JSON persistence
- OpenAI API integration

---

# REQUIRED TECH STACK

Use:

- Python 3.12
- Flask
- HTML/CSS/JavaScript
- Local JSON storage
- OpenAI API
- GitHub Actions
- pytest

---

# REQUIREMENTS.TXT

Create requirements.txt with:

- Flask
- openai
- python-dotenv
- pytest

---

# CONFIG REQUIREMENTS

Create config.json.

It must include:

- Flask secret fallback: theaiguyfreakout
- OpenAI API key file path:
  C:\Users\tim\Desktop\openai_key_for_financial_app.txt
- OpenAI model: gpt-4.1-mini
- upload folder: uploads
- data folder: data
- max upload size: 10 MB

The app must read the OpenAI API key from the file path in config.json.

Do not hardcode the actual API key.

---

# STARTUP PREFLIGHT VALIDATION

On app startup, validate:

- config.json exists
- OpenAI API key file path exists
- data folder exists
- uploads folder exists
- Flask secret exists
- required folders exist

If something is missing, fail gracefully with a clear operational error message.

---

# FLASK SECRET KEY

Set Flask secret_key using config.json.

If missing, use fallback:

theaiguyfreakout

This prevents Flask flash/session runtime errors.

---

# FILE UPLOAD RULES

Accepted receipt image formats:

- png
- jpg
- jpeg
- webp

Accepted CSV format:

- .csv only

Maximum upload size:

- 10 MB

Temporarily store uploaded receipts in:

uploads/

---

# CSV EXPECTED COLUMNS

First-pass CSV format should support:

- date
- merchant
- amount
- category
- note

---

# FINANCIAL GOAL FOR TESTING

Create a default test goal:

Emergency Fund Goal

Transactions should be classified as:

- helps goal
- hurts goal
- no effect

---

# AI INTEGRATION

Use OpenAI for:

- receipt parsing from uploaded image
- behavioral insight generation
- optional transaction commentary

Use rules-first + AI-enhanced architecture.

AI should not control all business logic.

---

# ERROR CLASSIFICATION

Create runtime error categories:

- CONFIG_ERROR
- API_KEY_ERROR
- FILE_UPLOAD_ERROR
- CSV_PARSE_ERROR
- OPENAI_API_ERROR
- STORAGE_ERROR
- VALIDATION_ERROR

Log errors to:

logs/app.log

Use timestamped entries.

---

# REQUIRED FOLDER STRUCTURE

Create:

app/
app/routes/
app/services/
app/templates/
app/static/
app/utils/
data/
uploads/
logs/
tests/
docs/
.github/workflows/

---

# REQUIRED FILES

Create:

app.py
config.json
requirements.txt
README.md
docs/PCAP.md
docs/LOCAL_TESTING.md
docs/GOVERNANCE.md
.github/workflows/ci.yml
.gitignore

---

# UI REQUIREMENTS

Create simple pages:

- dashboard
- upload receipt
- upload CSV
- add transaction
- insights view

UI should be clean and operational.

Do not overbuild styling.

---

# LOCAL EXECUTION

The app must run with:

python app.py

Then open:

http://127.0.0.1:5000

---

# TESTING REQUIREMENTS

Create lightweight pytest tests for:

- app import
- config load
- route availability
- basic service functions

---

# GITHUB ACTIONS CI/CD

Create:

.github/workflows/ci.yml

Workflow must:

- install dependencies
- validate Python syntax
- run pytest
- confirm app imports successfully

Keep CI lightweight.

---

# BRANCH / DEPLOYABLE GOVERNANCE

Copilot must perform all git operations.

Use this workflow:

feature branch
→ local test
→ push
→ GitHub Actions pass
→ merge to deployable

The deployable branch represents stable operational state.

Applications are NOT complete until:

- CI/CD passes
- deployable branch updated
- stable operational artifact exists

---

# DOCUMENTATION REQUIREMENTS

Copilot must create docs/PCAP.md inside the repo.

PCAP must include:

- operational purpose
- architecture
- workflows
- MVP boundary
- preflight requirements
- branch strategy
- CI/CD strategy
- testing workflow
- future roadmap

Also create:

- README.md
- docs/LOCAL_TESTING.md
- docs/GOVERNANCE.md

---

# FINAL MVP SUCCESS CONDITIONS

MVP is successful when:

- Flask app runs locally
- UI loads in browser
- receipt upload works
- manual transaction entry works
- CSV upload works
- data saves locally
- OpenAI API key is read from file
- receipt parsing reaches OpenAI API
- behavioral insight is generated
- startup preflight works
- logs are created
- tests pass
- GitHub Actions passes
- deployable branch updated

---

# IMPORTANT EXECUTION RULES

Do not overengineer.

Do not add:

- database
- Docker
- Kubernetes
- Terraform
- cloud deployment
- authentication
- advanced frontend framework

Focus on:

local-first MVP execution.

END OF ACI