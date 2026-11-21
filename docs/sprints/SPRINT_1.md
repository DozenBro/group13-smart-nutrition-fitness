# Sprint 1 Foundation and Health Tracking

**Draft 0.6 · 21 November 2026 · Partially implemented**

Read the [main specification](../PROJECT_SPEC.md) before taking a task. The original measurement baseline is `7e0f064`; source snapshot `a5de397` also includes the standalone S1-07 helper. Names follow the main specification roster. Start/review dates and task acknowledgements remain pending. Scope follows WBS 1.1–1.9 in the group plan.

**Start here:** [your first action](#first-action-for-each-member) · [database work](#database-deliverables-for-s1-03) · [task checklists](#implementation-checklists) · [review checklist](#review-checklist). The stories define required behavior; the task checklists explain how to deliver and verify it.

## Goal and Current Baseline

**Acceptance flow** — A Member registers, logs in, updates their profile, saves their own measurements, and views BMI/TDEE, history, and charts. An Admin lists, locks, and unlocks accounts.

**Available** — Shared measurement/BMI demo, PostgreSQL, migrations, validation, and a standalone proposed TDEE helper. The latest verified suite has 59 cases: 12 original measurement cases and 47 calculation cases. **Pending** — Accounts, ownership, profile/API/UI integration of TDEE, charts, administration, and team acceptance.

**S1-07 handover** — [PR #2](https://github.com/DozenBro/group13-smart-nutrition-fitness/pull/2) was merged into `main`. The [worked handover](../handover/S1-07_HEALTH_HANDOVER.md) is now available there. Merging code does not record a D-02 decision or acceptance of the complete US-H04 story; those still need explicit team evidence.

**Implementation order** — Finalize D-03, design authentication and its migrations, implement register/login/logout, protect measurement ownership, add profiles/TDEE, add charts and administration, then perform integration testing and review. Interface design and formula research can proceed in parallel.

## First Action for Each Member

**Tá Anh:** start S1-01 by reviewing the proposed health fields/rules with Tuấn Anh and Bảo. Record accepted and unresolved choices in D-02/S1-R01. Request Thắng's independent checks of S1-07. Your first handover is a field/rule list and expected examples, followed by the reviewed calculation contract.

**Tuấn Anh:** start S1-03 by drafting the ERD and field definitions below; draft D-03 alongside it. Agree API requests/responses with Bảo before implementing S1-04. You own backend profile endpoints as part of S1-04; Tá Anh supplies health rules and Bảo supplies the interface. Account/session work can proceed while profile-specific decisions are pending.

**Bảo:** start S1-02 with login/registration, profile, dashboard/history, and admin account screens, including error/empty/loading states. Show the prototype for review. Implement against the shared API contract after it is agreed; reuse the measurement demo where appropriate.

**Đạt:** draft the access-check scenarios for S1-06/S1-09 while reviewing S1-03/S1-04. Identify inputs, expected HTTP results, and expected unchanged data. Implement automated API permission tests with Tuấn Anh once endpoints are available; record concrete findings rather than only saying that the code was reviewed.

**Thắng:** independently calculate the S1-07 examples, then draft valid/invalid/missing-profile fixtures for S1-01/S1-05. Review Tá Anh's rules and Bảo's profile journey. Record expected versus observed results and issue links for failures.

**Hưng:** start S1-10 by reproducing setup from the README on another machine and checking CI. Record versions, commands, and actual results. Prepare browser acceptance steps and investigate D-06. Once features are integrated, verify them and coordinate S1-11 with Tá Anh.

**For everyone:** open or link an issue before starting, acknowledge your assignment and reviewer, add an actual due date, and use a task branch/PR following [GIT_WORKFLOW.md](../GIT_WORKFLOW.md). No task becomes Done just because these instructions were added.

| Team milestone | Value |
| --- | --- |
| Start date | To be filled |
| Review date | To be filled |
| Demo commit | To be recorded at acceptance |
| Coordinator | To be filled |

## User Stories and Acceptance Criteria

**AC** are verifiable acceptance criteria. A story reaches Done after meeting all its criteria and the shared Definition of Done. Stable IDs connect stories to code, tests, and logs.

### US-A01 Register an Account

**As a new user, I want to create an account so that I can use member features.** Owner Tuấn Anh, collaborating with Bảo, reviewer Đạt. Status Not started. WBS 1.6.

- **AC1** Valid registration creates a Member account that can be used to log in.
- **AC2** An existing email is rejected, including case variations according to the agreed rule.
- **AC3** Passwords are hashed using the selected library. API responses and application logs expose neither passwords nor hashes.
- **AC4** Registration input cannot grant Admin privileges to the applicant.

### US-A02 Log In and Log Out

**As a Member, I want to log in and log out so that I can access my data and end my session when finished.** Owner Tuấn Anh, collaborating with Bảo, reviewer Đạt. Status Not started. WBS 1.6. Depends on US-A01.

- **AC1** Correct credentials create a valid session that survives page refresh within its lifetime.
- **AC2** Incorrect credentials are rejected with a consistent message.
- **AC3** Logout invalidates the session at the backend. Reusing the old session for an API request is rejected.
- **AC4** Unauthenticated requests to protected features receive HTTP 401.
- **AC5** The backend enforces Admin authorization for direct API requests.

### US-H01 Update a Profile

**As a Member, I want to save profile information so that the system has the inputs needed for the agreed calculations.** Owner Tá Anh, collaborating with Tuấn Anh/Bảo, reviewer Thắng. Status Not started. WBS 1.7. Depends on US-A02 and D-02.

- **AC1** Fields, units, valid values, and required inputs are specified before the form is implemented.
- **AC2** A saved profile displays the same account's data after page refresh.
- **AC3** Invalid input produces an appropriate message and leaves the saved profile unchanged.
- **AC4** Another member cannot read or modify the profile by changing an ID in the request.

### US-H02 Record Body Measurements

**As a Member, I want to save weight and height so that I can track my changes over time.** Owners Tuấn Anh/Bảo, rules coordinated by Tá Anh, reviewer Đạt. Status Partial. WBS 1.7. Depends on US-A02.

- **AC1** Valid measurements are stored with their owner and a server-generated timestamp.
- **AC2** Records remain readable after page refresh and application restart.
- **AC3** Zero height and out-of-range input are rejected without creating a record.
- **AC4** The backend obtains ownership from the authenticated session. Submitting another user's `user_id` cannot create records on their behalf.
- **AC5** A failed save displays an error without presenting an unsaved record as successfully stored.

**Existing evidence** — Tests cover creation/retrieval and invalid input. Authentication and ownership are pending. Current tests cover parts of AC1–AC3.

### US-H03 View BMI

**As a Member, I want to view BMI from my measurements so that I can see the result of the system's formula.** Owners Tá Anh/Bảo, reviewer Thắng. Status Partial. WBS 1.7. Depends on US-H02.

- **AC1** 70 kg and 175 cm produce a displayed BMI of 22.86.
- **AC2** The backend converts centimetres to metres and applies the formula and rounding in S1-R02.
- **AC3** Results belong to the signed-in member's measurements. With no measurements, the screen prompts for input.
- **AC4** Tests use independently calculated examples and team-approved input boundaries.

### US-H04 View TDEE

**As a Member, I want to view estimated daily energy expenditure from my profile and measurements so that later planning features can use it.** Owner Tá Anh, collaborating with Tuấn Anh/Bảo, reviewer Thắng. Status Awaiting D-02. WBS 1.7.

The [S1-07 handover](../handover/S1-07_HEALTH_HANDOVER.md) proposes the equation, inputs, activity mapping, examples, and Python contract. This implements a calculation helper; it does not yet provide the Member-facing story or record human approval of D-02.

- **AC1** The team documents the equation, source, inputs, activity factors, applicable population, and rounding.
- **AC2** Unit tests verify at least two independently calculated examples before integration.
- **AC3** Missing required inputs identify the fields to complete and leave the result unavailable.
- **AC4** The interface shows kcal/day and identifies the value as an estimate.

### US-H05 View History and Charts

**As a Member, I want to view my measurement history and charts so that I can track recorded changes.** Owner Bảo, collaborating with Tuấn Anh, reviewer Hưng. Status Partial. WBS 1.7. Depends on US-H02.

- **AC1** The table and chart use measurements belonging to the current account.
- **AC2** The table defaults to newest first. The chart uses chronological order and labels units.
- **AC3** After saving and refreshing, the table and chart update from persisted data.
- **AC4** Empty, loading, and API error states are handled clearly.

**Existing evidence** — A shared history table is available. Ownership filtering and charts are pending.

### US-AD01 Manage Account Status

**As an Admin, I want to list, lock, and unlock accounts so that I can manage system access.** Owners Tuấn Anh/Bảo, reviewer Đạt. Status Not started. WBS 1.8. Depends on US-A02.

- **AC1** Admins can list accounts and their status, and lock/unlock accounts.
- **AC2** Members calling administration APIs directly receive HTTP 403.
- **AC3** A locked account cannot start a new session or use an old session to access protected APIs.
- **AC4** Unlocking an account allows login again and retains its previous data.
- **AC5** Account lists omit passwords and password hashes.

## Sprint 1 Rules

| ID | Rule | Status |
| --- | --- | --- |
| S1-R01 | Weight is greater than 0 and at most 500 kg. Height is 50–250 cm. Both allow at most 2 decimal places. | Used in the demo, limits await team confirmation |
| S1-R02 | BMI = kg / (cm / 100)². The backend rounds the displayed result to 2 decimal places using ROUND_HALF_UP. | Implemented with an example test |
| S1-R03 | Recording time is server-generated and timezone-aware. The current interface uses the viewer's local timezone. | Available in the demo, final display awaits D-05 |
| S1-R04 | Members read/write their own data using backend-authenticated identity. | Target requirement, implementation pending |
| S1-R05 | Admins manage account status. Locked users are denied access even through old sessions. | Target requirement, implementation pending |
| S1-R06 | Invalid data returns HTTP 422 with error information. Unauthenticated requests return 401 and unauthorized requests return 403. | 422 available, 401/403 pending |
| S1-R07 | Tests use `fitness_test`, separate from `fitness_demo`. | Implemented in the test command |

Update D-01–D-07 in the [shared decision table](../PROJECT_SPEC.md#open-decisions). Update sprint rules here and record changes in the revision history.

## API and Data

| Method and path | Input | Success | Errors |
| --- | --- | --- | --- |
| `POST /api/measurements` | JSON `weight_kg`, `height_cm` following S1-R01 | 201 with saved record and BMI | 422 invalid input, 503 database failure |
| `GET /api/measurements` | `limit` from 1 to 100, default 30 | 200 with records, newest first | 422 invalid limit, 503 database failure |
| `GET /docs` | Open in a browser | Swagger UI | Requires a running backend |

The request/response example uses fictional data. The system generates the actual `id` and timestamp.

```json
{"weight_kg": 70, "height_cm": 175}
```

```json
{
  "id": 1,
  "weight_kg": 70.0,
  "height_cm": 175.0,
  "bmi": 22.86,
  "created_at": "2026-11-19T04:00:00Z"
}
```

**Authentication changes** — Preserve valid save/read behavior and add session checks and ownership filtering to both endpoints. Tuấn Anh and Bảo document contracts for register/login/logout/current-user/profile/admin after D-03 is finalized, then use those contracts for implementation and tests.

### Data Model

The existing `measurements` table contains `id`, `weight_kg`, `height_cm`, and `created_at`. Database constraints enforce weight and height ranges. BMI is calculated when returning the result.

| Planned component | Design requirement |
| --- | --- |
| `users` | Primary key, unique normalized email, password hash, role, and locked status |
| `profiles` | One profile per user, with fields and limits following D-02 |
| `sessions` | User association, expiry, and revocation on logout or account locking |
| `measurements.user_id` | Foreign key to users, used for ownership checks |

Existing fictional records have no owner. Before the authentication migration, the team decides how to assign them to a demo account or otherwise handle them with the data holder's agreement. Record conversion steps and preservation checks in S1-03.

### Database Deliverables for S1-03

**Tuấn Anh prepares; Đạt reviews; Tá Anh and Bảo confirm the fields needed by calculations and screens.** Existing SQLAlchemy connection/model code and the initial measurement migration are starting points to extend.

- [ ] Produce `docs/design/SPRINT_1_ERD.md` with a readable ERD, primary/foreign keys, nullability, uniqueness, and relationship cardinalities.
- [ ] Detail `users`: identifier, normalized unique email, password hash, Member/Admin role, and locked status. Confirm email normalization and Admin creation in D-03 before freezing constraints.
- [ ] Detail `profiles`: a user relationship allowing at most one profile per account, calculation inputs following D-02, and the agreed incomplete-profile behavior. Do not guess age storage, supported values, or historical calculation policy.
- [ ] Detail `sessions` under the proposed server-session design: user association, identifier/storage policy, expiry, and revocation. Resolve D-03 before committing to the authentication design.
- [ ] Extend `measurements` with a user foreign key. Show one user to many measurements and sessions; enforce ownership in backend queries as well as relationships in the database.
- [ ] Extend `backend/models.py` and add the next Alembic migration under `migrations/versions/`. Keep the existing applied migration; document and implement an agreed conversion for ownerless fictional measurements before enforcing required ownership.
- [ ] Provide a documented, safe way to prepare fictional demo users/data, including a separate controlled Admin setup. Repeating data setup must not create duplicate accounts. Keep credentials out of the repository and record counts before/after upgrade.
- [ ] Verify both a clean `fitness_test` schema and an upgrade from the existing measurement schema using isolated test data. Record migration revision, steps, and preserved values/record ownership. Do not experiment with migration/reset commands against the working demo data.

The ERD may show future workout/meal modules at a high level to identify later relationships. Only the Sprint 1 account/profile/session/measurement structure is implemented in this task. The named tables are application tables; Alembic's version-tracking table is separate.

**Handover to Bảo/Đạt:** reviewed ERD and field list, migration/model PR, fictional-data setup instructions, and actual clean-install/upgrade results. A picture alone does not complete S1-03.

## Tasks and Assignments

Use **Not started → In progress → In review → Done**. Use **Blocked** with a reason and the person needed to help. Names are synchronized with the main specification. Owners acknowledge their tasks and reviewers confirm availability in the issue; deadlines remain to be filled.

| Task | Deliverable | Assigned owner / reviewer | Dependencies | Due | Status | Issue or PR |
| --- | --- | --- | --- | --- | --- | --- |
| S1-01 | Finalize criteria, limits, and D-01/D-02/D-07 | Tá Anh / Thắng | Team meeting | To be filled | Not started | Not created |
| S1-02 | Figma auth/profile/dashboard/admin and error states | Bảo / Tá Anh | Relevant parts of S1-01 | To be filled | Not started | Not created |
| S1-03 | User/profile/session/measurement ERD and migration | Tuấn Anh / Đạt | D-03, profile design | To be filled | Not started | Not created |
| S1-04 | Registration/login/logout/current-user/profile contracts and backend | Tuấn Anh / Đạt | D-03, S1-03; D-02 for profile fields | To be filled | Not started | Not created |
| S1-05 | Authentication and profile interface | Bảo + Tá Anh / Thắng | S1-04 contract, S1-02 | To be filled | Not started | Not created |
| S1-06 | Ownership filtering for measurements and cross-account tests | Tuấn Anh + Đạt / Tá Anh | S1-03, S1-04 | To be filled | Not started | Not created |
| S1-07 | Sourced TDEE equation, independent examples, and unit tests | Tá Anh / Thắng | D-02 | To be filled | In review; D-02 and human verification pending | [Issue #1](https://github.com/DozenBro/group13-smart-nutrition-fitness/issues/1), [PR #2](https://github.com/DozenBro/group13-smart-nutrition-fitness/pull/2) |
| S1-08 | BMI/TDEE dashboard and history chart | Bảo / Hưng | S1-06, S1-07 | To be filled | Not started | Not created |
| S1-09 | Admin lock/unlock and locked-user session tests | Tuấn Anh + Bảo / Đạt | S1-04 | To be filled | Not started | Not created |
| S1-10 | Second-machine setup, browser testing, and staging | Hưng / Bảo | D-06, integrated flow | To be filled | Not started | Not created |
| S1-11 | Sprint 1 review, feedback, and improvements | Tá Anh + Hưng / whole team | Acceptance results | To be filled | Not started | Not created |

Owners can split large tasks into smaller issues linked to the original task/story. Record contributions so the team can identify who analyzed, implemented, tested, and reviewed each part.

## Implementation Checklists

Use only the checklist for your task, plus its referenced stories and dependencies. Paths below are planned outputs unless already present; create them when doing the task. They are not claims that design, tests, or implementation already exist. Extend existing project files rather than starting another application.

If a named reviewer also authors part of a task, another teammate must review that person's changes. For example, Đạt may review backend behavior and write permission tests, but another member reviews Đạt's test PR.

### S1-01 Requirements and Input Rules

**Owner:** Tá Anh. **Reviewer:** Thắng. **Inputs:** the eight stories above, shared decisions, and S1-07 proposal.

- [ ] List profile and measurement fields with names, types, units, allowed values, required/optional status, and one valid/invalid example. Agree the fields with Tuấn Anh and Bảo before schema/form implementation.
- [ ] Record D-01/D-02/D-07 outcomes or precise unresolved questions, responsible people, and next action. Keep unresolved choices marked Proposed; leave dependent work visibly blocked where necessary.
- [ ] Link each story to its task, expected acceptance examples, owner/reviewer, and actual due date.

**Handover:** updated rule/decision sections and examples in this specification and the linked health handover. **Verified when:** Thắng records the review and Tuấn Anh/Bảo confirm they can implement the same fields/rules without guessing.

### S1-02 Screen Prototype

**Owner:** Bảo. **Reviewer:** Tá Anh. **Inputs:** S1-01 fields and story outcomes; draft API contract with Tuấn Anh.

- [ ] Sketch registration/login, profile, measurement/dashboard/history/chart, and admin account status screens in one linked Figma prototype or agreed equivalent.
- [ ] Show navigation and successful, invalid-input, empty, loading, unauthenticated, and API-error states relevant to each screen.
- [ ] Walk a teammate through the Member and Admin journeys; record feedback and changes.

**Handover:** prototype link/version and field/error-state notes in the task issue. **Verified when:** Tá Anh can follow the stories in the prototype and the displayed data matches the agreed field list.

### S1-03 Database and Migration

**Owner:** Tuấn Anh. **Reviewer:** Đạt. **Inputs:** D-03 and reviewed fields from S1-01/D-02.

- [ ] Complete the [database checklist](#database-deliverables-for-s1-03), including schema, constraints, ownerless-record conversion, fictional setup, and both migration checks.
- [ ] Review the ERD with Đạt and the profile/measurement fields with Tá Anh/Bảo before integrating the migration.

**Handover:** `docs/design/SPRINT_1_ERD.md`, model/migration code, data setup instructions, and verification evidence. **Verified when:** Đạt can reproduce creation/upgrade and account/measurement relationships from the instructions without losing test records.

### S1-04 Authentication and Profile Backend

**Owner:** Tuấn Anh. **Reviewer:** Đạt. **Inputs:** D-03, S1-03; reviewed D-02 fields for the profile portion.

- [ ] Agree and record registration, login, logout, current-user, profile read/update, and admin account-list/status API contracts with Bảo in `docs/design/SPRINT_1_API.md`. Include methods/paths, authentication, fields, success/error responses, and fictional examples.
- [ ] Implement the authentication/profile routes, schemas, and backend checks, extending the current FastAPI application. Hash passwords using the agreed maintained library, reject duplicate registrations, and prevent self-assigned Admin roles.
- [ ] Implement session expiry/revocation and safe initial Admin creation under D-03. Validate profile changes and keep stored data unchanged on rejection.
- [ ] Add appropriate tests, such as `tests/test_auth.py` and `tests/test_profiles.py`, for valid/invalid requests, logout, expiry, and profile persistence. Coordinate cross-account tests under S1-06.

**Handover:** API contract, migration-compatible backend, Swagger examples, and test/PR results. **Verified when:** Đạt reproduces the account/profile flows through direct API requests and Bảo can use the same contract without inventing fields or paths.

### S1-05 Authentication and Profile Interface

**Implementation lead:** Bảo. **Health-input support:** Tá Anh. **Backend dependency:** Tuấn Anh's S1-04 profile/authentication endpoints. **Reviewer:** Thắng.

- [ ] Implement the reviewed login/registration/profile screens and wire them to S1-04; keep input names and validation messages consistent with S1-01.
- [ ] Show session/loading/error states and saved profile data after refresh. Do not present a rejected or failed save as successful.
- [ ] Have Thắng try valid, missing, and invalid inputs using the expected fixtures and record observations/fixes.

**Handover:** frontend PR and tested journey/fixture results. **Verified when:** Thắng can register/login, save/reload a profile, and observe unchanged saved data after an invalid update.

### S1-06 Measurement Ownership and Permission Tests

**Backend lead:** Tuấn Anh. **Permission-test lead:** Đạt. **Reviewer:** Tá Anh. **Inputs:** S1-03/S1-04 and US-H02.

- [ ] Resolve account identity from the session and scope measurement writes/reads to that identity; apply equivalent cross-account protection to profiles.
- [ ] Add tests such as `tests/test_permissions.py`: no session is denied; two fictional accounts remain isolated; changing/submitting an owner identifier cannot read or write another account's records.
- [ ] Verify existing validation, save/read behavior, ordering/limits, and persistence still work after adding ownership. Record both permitted and rejected requests and their database effects.

**Handover:** protected routes and automated test results, reviewed by Tá Anh. **Verified when:** each account sees only its own records and failed cross-account requests leave data unchanged.

### S1-07 Calculation Review and Handover

**Owner:** Tá Anh. **Reviewer:** Thắng. **Integration reviewer:** Tuấn Anh. **Inputs:** D-02 and the merged helper/handover from PR #2.

- [ ] Review the existing [formula/input contract](../handover/S1-07_HEALTH_HANDOVER.md) rather than rewriting it. Thắng independently checks examples H-01/H-02 and rounding; record actual review conclusions.
- [ ] Resolve the proposed equation, activity mapping, age scope, profile age/history policy, and input limits with the group. Update D-02 and any affected tests if a rule changes.
- [ ] Run `tests/test_health.py` and hand the accepted function signature and expected examples to Tuấn Anh/Bảo. Track API/UI integration separately under S1-04/S1-08.

**Handover:** reviewed rule source/examples, health helper/tests, and explicit D-02 outcome. **Verified when:** Thắng's independent result agrees and the group decision is recorded. A merged helper alone does not finish this review or US-H04.

### S1-08 Health Dashboard and History Chart

**Owner:** Bảo. **Backend/calculation support:** Tuấn Anh/Tá Anh. **Reviewer:** Hưng. **Inputs:** S1-06, accepted S1-07 rules, and the shared API contract.

- [ ] Obtain the signed-in member's measurements and estimate from the agreed backend contract; Tuấn Anh integrates the health helper with the agreed profile/measurement selection. Missing inputs identify what to complete and leave TDEE unavailable.
- [ ] Display BMI, estimated TDEE in kcal/day, a newest-first table, and a chronological chart with date/unit labels. Agree the chart library only when needed and record the choice.
- [ ] Check no-history, one/multiple records, refresh after save, API failure, and narrow-screen behavior with Hưng. Match numeric output to reviewed fixtures.

**Handover:** working API-to-dashboard flow and observed browser results. **Verified when:** Hưng reproduces the correct owned data/chart after refresh and sees clear missing/error states.

### S1-09 Admin Account Status

**Backend lead:** Tuấn Anh. **Interface lead:** Bảo. **Permission-test/reviewer:** Đạt. **Inputs:** S1-04/D-03 and US-AD01.

- [ ] Implement the reviewed account-list/lock/unlock API and UI. Omit password/hash/session secrets from responses.
- [ ] Add direct API tests such as `tests/test_admin.py`: Member denied, Admin allowed, locked login denied, old sessions denied, unlocked account can log in, and prior records preserved.
- [ ] Have Đạt reproduce both the UI flow and direct API denial; UI visibility alone is not an authorization check.

**Handover:** admin API/UI, tests, and review evidence. **Verified when:** all US-AD01 criteria pass, including the old-session case.

### S1-10 Setup, CI, Browser Acceptance, and Staging

**Owner:** Hưng. **Reviewer:** Bảo. **Backend/setup support:** Tuấn Anh. **Inputs:** current README/launcher/CI and the integrated flow; D-06 for staging.

- [ ] Follow installation/startup on another machine and record versions, commands, results, and needed README fixes. Keep local demo/test data separate.
- [ ] Write `docs/testing/SPRINT_1_TEST_PLAN.md` with scenario, expected/actual result, tester/date, commit, and evidence. Cover the Sprint 1 stories, including invalid input and access denial; coordinate automated browser coverage as the UI becomes available.
- [ ] Verify the relevant GitHub Actions run for the demo commit and persistence after restart. Record exact CI/test links instead of a generic green-status claim.
- [ ] Resolve D-06 and verify staging setup/URL/persistence if available. If access is blocked, record the blocker and seek an explicit acceptance/scope decision; a local run does not automatically satisfy staging.

**Handover:** reproducible README, test plan/results, CI/browser evidence, and staging result or precise blocker. **Verified when:** Bảo reproduces setup and the acceptance checks, and the remaining environment limits are explicit.

### S1-11 Sprint Review and Handover

**Leads:** Tá Anh and Hưng. **Reviewers:** whole team. **Inputs:** acceptance evidence from S1-01 through S1-10.

- [ ] Execute the review checklist below against a named commit and identify Done, partial, blocked, and pending items accurately.
- [ ] Record the Member/Admin demo, ERD/API explanation, tests/CI, actual contributions, AI assistance, defects, and feedback in `docs/reviews/SPRINT_1_REVIEW.md`.
- [ ] Assign follow-up owners/dates and one concrete improvement for Sprint 2. Update task/story status only against acceptance evidence and the shared Definition of Done.

**Handover:** review report, demonstrated commit, traceable evidence, and revised backlog. **Verified when:** teammates can reproduce the reported results and every unfinished item has a clear next action.

## Testing and Acceptance

### Requirements and Evidence

| Story or foundation | Existing evidence | Additional acceptance evidence |
| --- | --- | --- |
| Measurement persistence | `test_save_then_read` | Restart app/database, compare records, and name the tester |
| US-H02 | `test_invalid_input_does_not_save` with 9 invalid inputs | Authentication, ownership, and save failures |
| US-H03 | `test_bmi_known_example`, `test_save_then_read` | Member-owned flow and agreed boundary cases |
| US-H05 | `test_newest_first_and_limit` | Ownership filtering, charts, and error/empty/loading states |
| US-A01, US-A02 | None yet | Duplicate email, invalid login, logout, expiry, and Admin permissions |
| US-H01, US-H04 | `tests/test_health.py`: independent TDEE fixtures, five factors, rounding, invalid inputs, and proposed age bounds | Human review of D-02/examples, profile/API integration, and cross-account access |
| US-AD01 | None yet | Member denial, old-session locking, unlocking, and data preservation |
| CI | EV-01 | Successful CI for the demonstrated commit |

Existing tests are in [tests/test_measurements.py](../../tests/test_measurements.py). Run from the repository root on Windows.

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Apply the [shared Definition of Done](../PROJECT_SPEC.md#definition-of-done). Stories involving authentication and private data must meet those criteria before completion.

### Review Checklist

- [ ] Show the backlog and identify completed, partial, and pending stories.
- [ ] Demonstrate registration/login, valid measurement saving, and retrieval after refresh.
- [ ] Demonstrate invalid input, rejection of cross-account access, and logout invalidating an old session.
- [ ] Compare BMI/TDEE with independent examples and show the history chart.
- [ ] Demonstrate Member denial on admin APIs, account locking/unlocking, and old-session checks.
- [ ] Show the ERD, API contracts, migrations, and tests/CI for the demo commit.
- [ ] Record feedback, open defects, and improvements for Sprint 2.

## Work Log and Evidence

### Verified Evidence

| ID | Date | Event | Verification source | Limits of the evidence |
| --- | --- | --- | --- | --- |
| EV-01 | 19 November 2026 | Build and test completed successfully at commit `a2e3eea` | [GitHub Actions run 44459130985](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/runs/44459130985) | Confirms frontend build, migration, and backend tests. Story review and acceptance require separate evidence |
| EV-02 | 19 November 2026 | Initial measurement/BMI code created with AI assistance at the user's request | Commit `cb29921`, backend/frontend/test/migration files in the repository | Team attribution to A–F is pending |

Earlier verification recorded 12 passing PostgreSQL tests and browser checks for saving, refresh, invalid input, and a narrow screen. Members should rerun the checks on their machines and record their names and results when accepting the handover.

### Member and AI Activity Log

Add an entry for each session producing a handover result, such as a rule decision, code change, test run, or review. Link longer records in issues/PRs. No session has yet been confirmed under the name of a member A–F.

Complete the template below or link the handover in its issue/PR. Use the S1-LOG prefix for this sprint.

```text
Log ID: S1-LOG-[sequence number]
Date, time, and timezone: [actual time]
Responsible member: [name and role]
Task / story / issue: [IDs and links]
Starting commit or branch: [actual value]
Goal: [expected outcome]
AI assistance: [tool, model if known, or none]
Request to AI: [summary or link, with secrets removed]
AI-generated work or proposals: [specific details]
What the member verified or changed: [specific details]
Changed files: [relative paths]
Verification commands or steps: [actually executed]
Results and evidence: [pass/fail/not run, link or short output]
Reviewer and conclusion: [name and conclusion, or awaiting review]
Handover commit / PR: [actual link, or unavailable]
Blockers and next steps: [if any]
```

| Log | Member | Task | Result summary | Evidence | Review status |
| --- | --- | --- | --- | --- | --- |
| No confirmed member entry yet | To be filled | To be filled | To be filled | To be filled | Awaiting entry |

### S1-LOG-001: AI-Assisted S1-07 Handover Example

- Date: 21 November 2026, Asia/Bangkok.
- Requested by: the user, for the health-module handover. Planned owner/reviewer remain Tá Anh/Thắng; neither person's independent execution or approval is claimed.
- Starting commit: `235be59`; branch: `feature/S1-07-tdee-handover`.
- Goal: create a sourced formula proposal, a pure TDEE helper, numerical/invalid-input tests, and a PR for integration review.
- AI assistance: source lookup, documentation, implementation, tests, and Git/PR preparation. The exact model identifier was not recorded.
- Verification: initial 9 calculation tests failed because the helper was absent, then passed after the calculation was added. A second run exposed 36 validation failures before input validation was implemented.
- Final local result: `python -m pytest -q tests/test_health.py` via the project venv: 47 passed. `python manage.py test` via the project venv and isolated `fitness_test`: 59 passed, with one pre-existing Starlette/httpx deprecation warning.
- Environment note: sandbox loopback access was denied; the authorized full test command succeeded outside that restriction.
- Remaining work: human arithmetic/rule review, D-02 decision, profile/schema/API/UI integration, permission tests, and Member-facing acceptance.
- Independent AI code review: the reviewer reran all 47 calculation cases and found no critical, important, or minor code findings. This is separate from the pending team review of D-02 and integration.
- Task tracking: [S1-07 issue #1](https://github.com/DozenBro/group13-smart-nutrition-fitness/issues/1).
- Handover: [PR #2](https://github.com/DozenBro/group13-smart-nutrition-fitness/pull/2), first implementation commit `31ad446`. Initially opened for review, then merged into `main` as `a5de397`. The merge was verified on 21 November 2026; it does not itself record Tuấn Anh/Thắng's review conclusions or a D-02 decision.

### S1-LOG-002: Task Checklist Clarification

- Date: 21 November 2026, Asia/Bangkok. Requested by the user after identifying unclear database/task handoffs.
- AI assistance: expanded existing S1-01 through S1-11 into owner/input/action/output/verification checklists; added each member's first action and explicit S1-03 database deliverables.
- Clarified backend profile ownership under Tuấn Anh's S1-04 and the S1-05 interface/health support split. Task/story IDs and acceptance criteria remain unchanged.
- Repository baseline: `a5de397`; documentation branch `docs/S1-action-checklists`. No implementation or schema changes are included in this clarification.
- Verification: task/role/dependency consistency, preserved story criteria, local links, and document structure are checked before committing. Human task acknowledgements, dates, decisions, implementation, and acceptance remain pending where not separately evidenced.

## Revision History

| Version | Date | Change | Confirmation |
| --- | --- | --- | --- |
| 0.1 | 19 November 2026 | Initial stories, criteria, and tasks in PROJECT_SPEC.md, baseline a2e3eea | Prepared with AI, awaiting team confirmation |
| 0.2 | 19 November 2026 | Split Sprint 1, retaining stories/criteria/tasks/evidence and adding the review checklist | Prepared with AI, awaiting team confirmation |
| 0.3 | 19 November 2026 | Translate into English and update navigation links | Awaiting team review |
| 0.4 | 20 November 2026 | Synchronize named owners and reviewers with the main specification roster | Names supplied by the user; task acknowledgements and reviews pending |
| 0.5 | 21 November 2026 | Add S1-07 formula proposal, handover, pure calculation evidence, and AI work log | Human review, D-02 approval, and integration pending |
| 0.6 | 21 November 2026 | Add member starting actions, explicit database handoff, and implementation/verification checklists for all 11 tasks; record PR #2 merge | Task acknowledgements and human decisions still require evidence |
