# Change Log

## 2026-05-21

- **MVP bootstrap created**: initial local Flask application scaffolded for Financial Intelligence App.
- **Local Flask app created**: core Flask routes, templates, and app startup flow established.
- **Browser UI created**: user-facing upload forms and dashboard views added.
- **Dashboard route created**: transaction dashboard introduced for viewing uploaded and parsed entries.
- **Upload receipt route created**: receipt image upload endpoint added.
- **Upload CSV route created**: transaction CSV ingestion flow implemented.
- **Add transaction route created**: manual entry support and transaction creation workflow added.
- **Insights view created**: aggregated insights and basic analytics surfaced in the app.
- **Local JSON persistence added**: transaction storage persisted in `data/transactions.json`.
- **Default Emergency Fund Goal added**: built-in savings goal support added to the dashboard.
- **GitHub Actions CI/CD created**: automated tests and validation introduced for every commit.
- **Deployable branch governance established**: branch promotion workflow and stable `deployable` branch policy defined.
- **OpenAI receipt parsing feature added**: AI-powered receipt extraction integrated as a service.
- **OpenAI SDK v1 compatibility fix added**: receipt parser updated to modern OpenAI SDK client syntax.
- **OpenAI model changed to `gpt-4o-mini`**: invalid model replaced with a validated production-accessible model.
- **JSON response parsing reliability improved**: safe JSON parsing, markdown fence stripping, and fallback handling added.
- **Successful Walmart receipt parsing validated**: operational validation confirmed merchant, category, amount, subtotal, tax, and total extraction.
- **Dashboard successfully displayed parsed merchant, category, amount, subtotal, tax, and total**: end-to-end receipt parsing output verified in UI.
- **Clean MVP UI theme implemented**: professional light-themed interface with improved readability, consistent navigation, and polished styling applied across all pages.
- **Deployable promotion prepared**: first operational AI-powered Financial Nebula Node MVP ready for deployable merge with validated receipt parsing, governance tracking, and CI/CD workflow.

## 2026-05-22

- **Docker containerization support added**: Dockerfile, dockerignore, and container usage docs created for consistent local container testing without baking secrets.
