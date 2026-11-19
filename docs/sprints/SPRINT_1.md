# Sprint 1 Foundation and Health Tracking

**Draft 0.3 · 19 November 2026 · Partially implemented**

Read the [main specification](../PROJECT_SPEC.md) before taking a task. The code baseline is `7e0f064`. The team must confirm start/review dates and member names. Scope follows WBS 1.1–1.9 in the group plan.

## Goal and Current Baseline

**Acceptance flow** — A Member registers, logs in, updates their profile, saves their own measurements, and views BMI/TDEE, history, and charts. An Admin lists, locks, and unlocks accounts.

**Available** — Shared measurement/BMI demo, PostgreSQL and migrations, input validation, 12 test cases, and successful CI. **Pending** — Accounts, ownership, profiles/TDEE, charts, administration, and team acceptance.

**Implementation order** — Finalize D-03, design authentication and its migrations, implement register/login/logout, protect measurement ownership, add profiles/TDEE, add charts and administration, then perform integration testing and review. Interface design and formula research can proceed in parallel.

| Team milestone | Value |
| --- | --- |
| Start date | To be filled |
| Review date | To be filled |
| Demo commit | To be recorded at acceptance |
| Coordinator | To be filled |

## User Stories and Acceptance Criteria

**AC** are verifiable acceptance criteria. A story reaches Done after meeting all its criteria and the shared Definition of Done. Stable IDs connect stories to code, tests, and logs.

### US-A01 Register an Account

**As a new user, I want to create an account so that I can use member features.** Proposed owner B, collaborating with C, reviewer D. Status Not started. WBS 1.6.

- **AC1** Valid registration creates a Member account that can be used to log in.
- **AC2** An existing email is rejected, including case variations according to the agreed rule.
- **AC3** Passwords are hashed using the selected library. API responses and application logs expose neither passwords nor hashes.
- **AC4** Registration input cannot grant Admin privileges to the applicant.

### US-A02 Log In and Log Out

**As a Member, I want to log in and log out so that I can access my data and end my session when finished.** Owner B, collaborating with C, reviewer D. Status Not started. WBS 1.6. Depends on US-A01.

- **AC1** Correct credentials create a valid session that survives page refresh within its lifetime.
- **AC2** Incorrect credentials are rejected with a consistent message.
- **AC3** Logout invalidates the session at the backend. Reusing the old session for an API request is rejected.
- **AC4** Unauthenticated requests to protected features receive HTTP 401.
- **AC5** The backend enforces Admin authorization for direct API requests.

### US-H01 Update a Profile

**As a Member, I want to save profile information so that the system has the inputs needed for the agreed calculations.** Owner A, collaborating with B/C, reviewer E. Status Not started. WBS 1.7. Depends on US-A02 and D-02.

- **AC1** Fields, units, valid values, and required inputs are specified before the form is implemented.
- **AC2** A saved profile displays the same account's data after page refresh.
- **AC3** Invalid input produces an appropriate message and leaves the saved profile unchanged.
- **AC4** Another member cannot read or modify the profile by changing an ID in the request.

### US-H02 Record Body Measurements

**As a Member, I want to save weight and height so that I can track my changes over time.** Owners B/C, rules coordinated by A, reviewer D. Status Partial. WBS 1.7. Depends on US-A02.

- **AC1** Valid measurements are stored with their owner and a server-generated timestamp.
- **AC2** Records remain readable after page refresh and application restart.
- **AC3** Zero height and out-of-range input are rejected without creating a record.
- **AC4** The backend obtains ownership from the authenticated session. Submitting another user's `user_id` cannot create records on their behalf.
- **AC5** A failed save displays an error without presenting an unsaved record as successfully stored.

**Existing evidence** — Tests cover creation/retrieval and invalid input. Authentication and ownership are pending. Current tests cover parts of AC1–AC3.

### US-H03 View BMI

**As a Member, I want to view BMI from my measurements so that I can see the result of the system's formula.** Owners A/C, reviewer E. Status Partial. WBS 1.7. Depends on US-H02.

- **AC1** 70 kg and 175 cm produce a displayed BMI of 22.86.
- **AC2** The backend converts centimetres to metres and applies the formula and rounding in S1-R02.
- **AC3** Results belong to the signed-in member's measurements. With no measurements, the screen prompts for input.
- **AC4** Tests use independently calculated examples and team-approved input boundaries.

### US-H04 View TDEE

**As a Member, I want to view estimated daily energy expenditure from my profile and measurements so that later planning features can use it.** Owner A, collaborating with B/C, reviewer E. Status Awaiting D-02. WBS 1.7.

- **AC1** The team documents the equation, source, inputs, activity factors, applicable population, and rounding.
- **AC2** Unit tests verify at least two independently calculated examples before integration.
- **AC3** Missing required inputs identify the fields to complete and leave the result unavailable.
- **AC4** The interface shows kcal/day and identifies the value as an estimate.

### US-H05 View History and Charts

**As a Member, I want to view my measurement history and charts so that I can track recorded changes.** Owner C, collaborating with B, reviewer F. Status Partial. WBS 1.7. Depends on US-H02.

- **AC1** The table and chart use measurements belonging to the current account.
- **AC2** The table defaults to newest first. The chart uses chronological order and labels units.
- **AC3** After saving and refreshing, the table and chart update from persisted data.
- **AC4** Empty, loading, and API error states are handled clearly.

**Existing evidence** — A shared history table is available. Ownership filtering and charts are pending.

### US-AD01 Manage Account Status

**As an Admin, I want to list, lock, and unlock accounts so that I can manage system access.** Owners B/C, reviewer D. Status Not started. WBS 1.8. Depends on US-A02.

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

**Authentication changes** — Preserve valid save/read behavior and add session checks and ownership filtering to both endpoints. B and C document contracts for register/login/logout/current-user/profile/admin after D-03 is finalized, then use those contracts for implementation and tests.

### Data Model

The existing `measurements` table contains `id`, `weight_kg`, `height_cm`, and `created_at`. Database constraints enforce weight and height ranges. BMI is calculated when returning the result.

| Planned component | Design requirement |
| --- | --- |
| `users` | Primary key, unique normalized email, password hash, role, and locked status |
| `profiles` | One profile per user, with fields and limits following D-02 |
| `sessions` | User association, expiry, and revocation on logout or account locking |
| `measurements.user_id` | Foreign key to users, used for ownership checks |

Existing fictional records have no owner. Before the authentication migration, the team decides how to assign them to a demo account or otherwise handle them with the data holder's agreement. Record conversion steps and preservation checks in S1-03.

## Tasks and Assignments

Use **Not started → In progress → In review → Done**. Use **Blocked** with a reason and the person needed to help. Tasks, names, and deadlines await member confirmation.

| Task | Deliverable | Proposed owner / reviewer | Dependencies | Due | Status | Issue or PR |
| --- | --- | --- | --- | --- | --- | --- |
| S1-01 | Finalize criteria, limits, and D-01/D-02/D-07 | A / E | Team meeting | To be filled | Not started | Not created |
| S1-02 | Figma auth/profile/dashboard/admin and error states | C / A | Relevant parts of S1-01 | To be filled | Not started | Not created |
| S1-03 | User/profile/session/measurement ERD and migration | B / D | D-03, profile design | To be filled | Not started | Not created |
| S1-04 | Register/login/logout/current-user contracts and backend | B / D | D-03, S1-03 | To be filled | Not started | Not created |
| S1-05 | Authentication and profile interface | C + A / E | S1-04 contract, S1-02 | To be filled | Not started | Not created |
| S1-06 | Ownership filtering for measurements and cross-account tests | B + D / A | S1-03, S1-04 | To be filled | Not started | Not created |
| S1-07 | Sourced TDEE equation, independent examples, and unit tests | A / E | D-02 | To be filled | Not started | Not created |
| S1-08 | BMI/TDEE dashboard and history chart | C / F | S1-06, S1-07 | To be filled | Not started | Not created |
| S1-09 | Admin lock/unlock and locked-user session tests | B + C / D | S1-04 | To be filled | Not started | Not created |
| S1-10 | Second-machine setup, browser testing, and staging | F / C | D-06, integrated flow | To be filled | Not started | Not created |
| S1-11 | Sprint 1 review, feedback, and improvements | A + F / whole team | Acceptance results | To be filled | Not started | Not created |

Owners can split large tasks into smaller issues linked to the original task/story. Record contributions so the team can identify who analyzed, implemented, tested, and reviewed each part.

## Testing and Acceptance

### Requirements and Evidence

| Story or foundation | Existing evidence | Additional acceptance evidence |
| --- | --- | --- |
| Measurement persistence | `test_save_then_read` | Restart app/database, compare records, and name the tester |
| US-H02 | `test_invalid_input_does_not_save` with 9 invalid inputs | Authentication, ownership, and save failures |
| US-H03 | `test_bmi_known_example`, `test_save_then_read` | Member-owned flow and agreed boundary cases |
| US-H05 | `test_newest_first_and_limit` | Ownership filtering, charts, and error/empty/loading states |
| US-A01, US-A02 | None yet | Duplicate email, invalid login, logout, expiry, and Admin permissions |
| US-H01, US-H04 | None yet | Valid/invalid profiles, cross-account access, and independent TDEE examples |
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

## Revision History

| Version | Date | Change | Confirmation |
| --- | --- | --- | --- |
| 0.1 | 19 November 2026 | Initial stories, criteria, and tasks in PROJECT_SPEC.md, baseline a2e3eea | Prepared with AI, awaiting team confirmation |
| 0.2 | 19 November 2026 | Split Sprint 1, retaining stories/criteria/tasks/evidence and adding the review checklist | Prepared with AI, awaiting team confirmation |
| 0.3 | 19 November 2026 | Translate into English and update navigation links | Awaiting team review |
