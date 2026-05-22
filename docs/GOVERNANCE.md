# Governance

## Branch Strategy

- **Feature branches**: Use descriptive names, e.g., `feature/csv-upload`, `fix/config-error`
- **Local testing**: Test all flows locally before push
- **GitHub Actions CI**: All commits trigger CI (syntax check, import test, pytest)
- **Deployable branch**: Merge feature branch to `deployable` only after CI passes
- **Deployable = Stable**: Only production-ready, tested code

## Commit Standards

- Clear, descriptive commit messages
- One logical change per commit
- Reference issue/task if applicable

Example:
```
feat: add preflight validation for config and API key
- validate config.json on startup
- check OpenAI API key file exists
- log errors with timestamps
```

## Operational Discipline

- Do NOT merge to deployable until CI passes
- Keep changes minimal and focused on MVP scope
- All git operations performed by Copilot workflow automation
- No manual hotfixes to deployable branch

## OpenAI SDK Compatibility Governance

- Do not pin legacy SDK versions unless explicitly approved
- Prefer modern SDK-compatible code over downgrading dependencies
- Fix code to support the current OpenAI SDK
- Log SDK compatibility issues and document fixes

## AI Response Format Governance

- AI responses used by application logic must be constrained, validated, and safely parsed before use
- Prefer strict JSON response instructions for structured outputs
- Handle markdown wrappers, empty responses, and malformed JSON with fallback behavior
- Log response length, preview, and validation outcome without exposing secrets

## Operational Logs Governance

- Every feature add must update `CHANGELOG.md`.
- Every runtime bug must update `docs/BUG_FIX_LOG.md`.
- Every AI/Copilot execution failure should be classified and logged.
- Logs should support future troubleshooting, passdowns, and operational continuity.

## UI Governance

- MVP UI must remain functional-first and professional.
- UI must not imply features that do not exist.
- Visual improvements should support operational clarity and readability.
- Keep styling lightweight and maintainable (CSS-only, no complex frameworks).
- Use feature branches for all UI changes and validate locally before merging.
- Avoid flashy animations, dark-mode-only designs, or overbuilt dashboard widgets.

## MVP Scope Lock

Do NOT add:
- Database
- Docker/containers
- Authentication
- Advanced UI frameworks
- Microservices
- Cloud infrastructure

Focus on: local-first, operationally testable execution.
