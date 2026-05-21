# Bug Fix Log

## 2026-05-21

### Bug 1 — Flask Secret Key Missing
- **Category:** runtime bug
- **Description:** `RuntimeError: The session is unavailable because no secret key was set.`
- **Impact:** Flash messages and session-related functionality failed, blocking user feedback and UI state.
- **Fix:** Added Flask `secret_key` fallback using config value `theaiguyfreakout`.
- **Validation Status:** fixed and validated locally.
- **Governance Lesson:** Flask apps using `flash`/`session` must include `secret_key` in preflight validation.

### Bug 2 — Deprecated OpenAI SDK Syntax
- **Category:** dependency compatibility bug
- **Description:** `openai.ChatCompletion` is no longer supported in `openai>=1.0.0`.
- **Impact:** OpenAI receipt parsing failed at runtime due to outdated SDK usage.
- **Fix:** Updated OpenAI service to use modern OpenAI SDK client syntax and `OpenAI(api_key=...)`.
- **Validation Status:** fixed and validated with mocked unit tests.
- **Governance Lesson:** Do not pin legacy SDK versions unless explicitly approved. Prefer modern SDK-compatible code.

### Bug 3 — Invalid OpenAI Model Name
- **Category:** configuration bug
- **Description:** The model `gpt-4-mini` does not exist or user does not have access.
- **Impact:** OpenAI requests failed with `model_not_found`, preventing receipt parsing.
- **Fix:** Changed model to `gpt-4o-mini` in `config.json` and service defaults.
- **Validation Status:** fixed, pushed, and operationally validated locally.
- **Governance Lesson:** Model availability must be verified as part of preflight execution readiness.

### Bug 4 — OpenAI Response JSON Parse Failure
- **Category:** validation bug
- **Description:** `Failed to parse OpenAI response as JSON` when the model returned non-strict JSON output.
- **Impact:** Receipt parsing failed even though OpenAI returned a response, causing fallback behavior.
- **Fix:** Improved JSON response handling with prompt instructions, markdown fence stripping, empty response detection, safe parsing, and fallback logging.
- **Validation Status:** fixed and validated with additional unit tests.
- **Governance Lesson:** AI outputs used by application logic must be constrained, validated, and safely parsed.
