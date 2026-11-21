# TDEE Handover Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task by task. Steps use checkbox syntax for tracking.

**Goal:** Provide a reviewable S1-07 example with sourced rules, a pure calculation, tests, and a GitHub PR.

**Architecture:** Extend the existing health module with a keyword-only Decimal calculation. Keep APIs, schemas, authentication, UI, and approval of D-02 outside this change. Work on the requested task branch in the existing clean checkout.

**Tech Stack:** Python 3.14, Decimal, pytest, Git, GitHub.

**Spec:** [Health handover](../../handover/S1-07_HEALTH_HANDOVER.md), [Sprint 1](../../sprints/SPRINT_1.md), and the shared D-02 decision.

## Global Constraints

- English code and documentation; keep existing BMI behavior and measurement endpoints unchanged.
- All rule choices are proposed; no invented human review or accepted story status.
- Decimal measurements follow existing demo ranges/precision; no arbitrary activity factor supplied by the caller.
- Tests involving PostgreSQL use `fitness_test` through `manage.py test`.
- Push only the task branch; open the requested PR and leave merging to human review.

## Review Focus

- Missing, wrong-type, and non-finite inputs must fail predictably without a made-up estimate.
- Unknown equation/activity codes must not silently select another rule.
- Age boundaries and boolean-as-integer inputs must follow the documented scope.
- Rounding happens after multiplication; invalid non-positive REE is rejected.
- Documentation and PR must separate a proposed pure helper from API integration and human acceptance.

## Task 1: Calculation, tests, and handover

**Files:** modify `backend/health.py`, `docs/PROJECT_SPEC.md`, and `docs/sprints/SPRINT_1.md`; create `tests/test_health.py` and `docs/handover/S1-07_HEALTH_HANDOVER.md`.

**Interface:** `calculate_tdee(*, weight_kg: Decimal, height_cm: Decimal, age_years: int, sex_for_equation: str, activity_level: str) -> Decimal`; invalid inputs raise `ValueError`. Exact formulas, codes, ranges, and examples are in the linked handover.

- [x] Write numeric tests for H-01/H-02, five factors, age boundaries, and final-only HALF_UP rounding. Observe failure because the helper is absent.
- [x] Implement the minimal calculation, then run the numeric tests.
- [x] Add invalid-input tests: missing values, measurement boundaries/precision/types/non-finite values, age bounds/fraction/bool, unsupported codes, and non-positive REE. Observe these fail before adding validation.
- [x] Implement field validation, run calculation tests, then the complete suite. Expected: all pass; report the pre-existing Starlette/httpx deprecation warning.
- [x] Link the handover from shared D-02 and Sprint 1; keep approval and full US-H04 integration pending. Record actual AI assistance and verification in the sprint log.
- [x] Review all changes, commit, push the task branch, and open a PR with source links, verification, integration instructions, and the human review checklist.
- [x] Confirm the remote PR head and report its URL. Do not merge the PR or claim human acceptance.

## Execution Record

- Baseline: commit `235be59`, clean checkout, 12 tests passed against `fitness_test`; one existing Starlette/httpx warning.
- Environment: sandbox blocked loopback PostgreSQL; the authorized test command succeeded outside that restriction.
- User requested a complete worked example including branch and PR; execute directly, with team decisions left proposed for PR review.
- Verification: first 9 numeric cases RED then GREEN; validation cycle 36 RED then GREEN. Final calculation suite 47 passed; complete isolated-database suite 59 passed with the existing Starlette/httpx warning.
- Independent AI code review: no critical, important, or minor findings; 47 cases rerun by the reviewer. Clinical/product approval, authenticated integration, and remote PR verification remain outside that code-review conclusion.
- Task issue: https://github.com/DozenBro/group13-smart-nutrition-fitness/issues/1.
- Pull request: https://github.com/DozenBro/group13-smart-nutrition-fitness/pull/2. Verified open and unmerged; initial remote head `31ad446e6857c117838d66cda935ebbcf9096b2a`. This follow-up records the review links on the same branch.
