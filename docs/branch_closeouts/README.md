# Branch Closeouts

This folder stores closeout records for feature branches that are no longer active. Closed branches are historical artifacts only and should not receive new work.

Each closeout file documents the branch lifecycle and final status. Closeout records must follow the repository governance and be created on an administrative branch (e.g., `feature/branch-closeout-governance`).

Closeout filenames use the pattern:

```
<branch-name>_closeout.md
```

Example:

```
feature/test-aiw-error-reporting_closeout.md
```

Rules:
- Do NOT delete remote branches in this ACI.
- If uncertain about a branch's status, mark it `NEEDS_USER_REVIEW`.
- The `deployable` branch is protected and MUST NOT be modified.

For more details, see `docs/GOVERNANCE.md`.
