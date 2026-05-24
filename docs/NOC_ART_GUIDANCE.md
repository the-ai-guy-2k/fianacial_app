# N.O.C. ART GUIDANCE — Branch Closeout + AIW Success Report Guidance

DATE: 2026-05-24

PURPOSE

Update N.O.C. Art Guidance so branch closeout behavior is explicit and repeatable.

BRANCH CLOSEOUT CLARIFICATION

Branch closeout requires TWO things:

1. Central closeout documentation
2. Closeout commit on the actual branch being closed

Creating only `docs/branch_closeouts/` on an admin branch is NOT enough if the goal is for the closed branch itself to visibly show a final closeout state.

REQUIRED BRANCH CLOSEOUT BEHAVIOR

For each branch being closed, the AIW must:

1. Checkout the branch being closed.
2. Add or update a closeout marker file on that branch.
   Recommended file: `BRANCH_CLOSED.md` or `docs/branch_closeout.md`
3. Commit the closeout marker directly on that branch.
4. Use a clear closeout commit message.
5. Push that branch.
6. Then update central closeout documentation from the admin/governance branch if needed.

REQUIRED CLOSEOUT COMMIT MESSAGE FORMAT

Commit message:

Close out branch: <branch-name>

Commit body must include:

- Branch purpose:
  <why this branch was created>

- Mission status:
  COMPLETED / PARTIAL / ABANDONED / TEST_ONLY

- Merge status:
  MERGED / NOT_MERGED / SUPERSEDED / NEEDS_REVIEW

- Operational state:
  CLOSED

- Closeout record:
  <path to closeout doc if applicable>

- Rule:
  No further development should continue on this branch.

IMPORTANT RULE

A branch is not fully closed unless the branch itself contains a visible closeout commit or closeout marker.
Central documentation alone is useful, but it does not make the branch self-explanatory when viewed later in GitHub.

AIW SUCCESS REPORT GUIDANCE

When an ACI completes successfully, the AIW should create a success report.

Recommended folder:

`docs/aiw_success/`

Recommended filename pattern:

`YYYY-MM-DD_short-success-name.md`

Required sections:

# AIW SUCCESS REPORT

## Mission Status
COMPLETED / PARTIAL / BLOCKED / FAILED / NEEDS_REVIEW

## Summary

## Business / Operational Value

## What Changed

## Validation

## Current State

## Next Step

## Risk / Safety Notes

OPERATOR SUCCESS CRITERIA

After reading the AIW success report, the operator should be able to answer within 30 seconds:

- What happened?
- Did it work?
- What changed?
- How was it verified?
- What is the current state?
- What happens next?
- Are there risks?

RELATIONSHIP TO AIW TELEMETRY

`docs/aiw_errors/` = failure telemetry

`docs/aiw_success/` = success telemetry

`docs/branch_closeouts/` = branch lifecycle telemetry

Together these support:
- operational continuity
- manager visibility
- AIW accountability
- anti-drift stabilization
- repo lifecycle clarity

N.O.C. ART GUIDANCE REQUIREMENT

Future N.O.C. artifacts should include this branch closeout guidance so AIWs automatically understand that completed branches require:

- central closeout documentation
- branch-local closeout commit
- clear mission status
- clear no-further-work instruction

END UPDATE
