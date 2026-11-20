# Sprint 2 Workout Planning and Streaks

**Draft 0.3 · 20 November 2026 · Implementation pending**

Read the [main specification](../PROJECT_SPEC.md) and the authentication/ownership sections of [Sprint 1](SPRINT_1.md). This draft expands WBS 2.1–2.8 for refinement. Named owners and reviewers follow the main specification roster. Task acknowledgements, reviewer availability, dates, and algorithms require confirmation.

## Goal and Dependencies

**Demo flow** — Member selects a goal → receives a saved schedule → views session details → records completion → sees the correct streak.

The integrated flow uses Sprint 1 accounts and ownership. Exercise data, prototypes, templates, and independent algorithm tests can be prepared while authentication is being completed.

| Item | Value |
| --- | --- |
| Start / review date | To be filled |
| Coordinator | To be filled |
| Demo commit / review result | Unavailable |
| Inputs from Sprint 1 | Authentication, ownership, migrations, and CI |

## User Stories and Acceptance Criteria

### US-AD02 Manage the Exercise Catalog

**As an Admin, I want to manage exercises and categories so that the system has data for workout planning.** Owner Đạt, collaborating with Bảo, reviewer Tuấn Anh. Status Not started. WBS 2.3.

- **AC1** Admins create, read, update, and delete/archive exercises and categories according to the agreed policy.
- **AC2** Names, categories, equipment, difficulty, instructions, activity units, and sources are validated against the data template.
- **AC3** Members calling administration APIs are rejected. Exercise edits retain the content of existing plans and logs.
- **AC4** A reviewed seed dataset is imported. The provisional target is 40 exercises, pending S2-D04.

### US-W01 Obtain and View a Goal-Based Plan

**As a Member, I want a schedule matching my goal so that I know what to do each day.** Owner Đạt, collaborating with Bảo, reviewer Tá Anh. Status Not started. WBS 2.4–2.5.

- **AC1** Weight loss, muscle gain, and maintenance each produce a valid plan when enough data is available.
- **AC2** The plan specifies days/sessions, exercises, sets, and repetitions or duration according to the agreed template.
- **AC3** Missing or invalid goals are rejected. Insufficient matching exercises produce a clear message.
- **AC4** Plans are saved, readable after refresh, and accessible only by their owner.
- **AC5** Exercise selection can be explained using its rule/template. Changes to an existing plan follow S2-D01.

### US-W04 Record Workout Completion

**As a Member, I want to mark a workout session complete so that my activity is recorded.** Owner Đạt, collaborating with Bảo, reviewer Tuấn Anh. Status Not started. WBS 2.6.

- **AC1** Only the owner can complete a session on an allowed date.
- **AC2** The saved completion state persists after refresh.
- **AC3** Double clicks, retries, and two concurrent requests create only one completion for the same session.
- **AC4** Save failures do not display false success. Logs and activity data remain consistent when an operation fails.
- **AC5** Activity dates follow the agreed rule so Sprint 3 can reuse it.

### US-S01 View the Activity Streak

**As a Member, I want to view consecutive active days so that I can track my habits.** Owner Đạt, reviewer Hưng. Status Not started. WBS 2.6, extended in 3.4.

- **AC1** Completing multiple sessions on one date contributes one active day.
- **AC2** Consecutive active dates extend the streak. After a full missed date, the next activity starts a new streak.
- **AC3** Before today's first activity, display the state defined by S2-D03 without treating today as already missed.
- **AC4** Tests cover the first day, duplicate dates, consecutive dates, missed dates, midnight, and concurrent requests.
- **AC5** The streak can be reconciled with logs. Private data is accessible only to its account owner.

## Rules and Decisions

| ID | Proposal | Status / owner |
| --- | --- | --- |
| S2-D01 | Use reviewed templates for three goals. Define schedules, selection, units, rest between sessions, and plan regeneration/replacement | Awaiting Đạt + Tá Anh |
| S2-D02 | Define catalog fields, deletion/archiving, and history preservation after catalog edits | Awaiting Đạt + Tuấn Anh |
| S2-D03 | Confirm timezone with D-05, allowed completion dates, and undo/backdating. Proposed basis is server dates, counted once per day | Awaiting Đạt + Tá Anh |
| S2-D04 | Confirm the damaged CSV symbol before 40. Use 40 exercises as the provisional seed target | Awaiting Tá Anh |

**Proposed streak calculation** — Obtain distinct dates with valid activity. If today is active, count the sequence ending today. Otherwise, if yesterday is active, retain the sequence ending yesterday. Other cases return 0. A new activity after a missed date starts a streak of 1.

Confirm S2-D03 before using this calculation as a test oracle. Tests use a fixed clock. Sprint 3 references this rule when adding meals.

## Design and Planned Contracts

| Component | Design deliverable |
| --- | --- |
| UI | Figma goal selection, weekly schedule, session details, completion, and errors |
| Database | exercises/categories, workout_plans, workout_sessions, plan_items, workout_logs, and activity storage/retrieval |
| Integrity | Foreign keys, ownership, history rules, and unique completion per user/session |
| API | Exercise administration, plan creation/retrieval, session completion, and streak contracts |
| Sequence diagram | Completion flow, authorization, log storage, and activity calculation/update |

These API groups define planned design work. Record methods/paths, requests/responses, errors, and examples in the design issue before frontend/backend integration. Reuse Sprint 1 authentication. Migrations must preserve existing account and measurement data.

### Exercise Data Template

`id`, `name`, `category`, `equipment`, `difficulty`, `instructions`, `goal_tags`, `source`, `review_status`. Prescriptions such as sets/reps/duration belong in templates or plan items where appropriate. Each batch has separate data-entry and review owners.

## Tasks and Assignments

| Task | Deliverable | Assigned owner / reviewer | Dependencies | Due | Status | Issue/PR |
| --- | --- | --- | --- | --- | --- | --- |
| S2-01 | Prototype and story/workout/streak rule refinement | Bảo + Đạt / Tá Anh | Sprint 1 feedback | To be filled | Not started | Not created |
| S2-02 | ERD v2, migrations, contracts, and sequence diagram | Đạt + Tuấn Anh / Hưng | S2-D01–S2-D03 | To be filled | Not started | Not created |
| S2-03 | Admin catalog and reviewed seed dataset | Đạt + Bảo / Thắng | S2-02, S2-D04 | To be filled | Not started | Not created |
| S2-04 | Plan generation and tests for three goals/insufficient data | Đạt / Tá Anh | S2-02, trial data | To be filled | Not started | Not created |
| S2-05 | Weekly schedule and plan details from the API | Bảo / Đạt | S2-02 contracts, S2-04 | To be filled | Not started | Not created |
| S2-06 | Completion/streak logic and duplicate/date/permission tests | Đạt / Tuấn Anh + Hưng | S2-04, S2-D03 | To be filled | Not started | Not created |
| S2-07 | Integration, Sprint 1 regression, and data-preserving migration tests | Hưng + Tá Anh / Tuấn Anh | Integrated flow | To be filled | Not started | Not created |
| S2-08 | Review, feedback, challenge decision, and Sprint 3 planning | Tá Anh + Hưng / whole team | S2-07, D-04 | To be filled | Not started | Not created |

## Testing and Review

| Story | Required checks | Current evidence |
| --- | --- | --- |
| US-AD02 | Admin CRUD, Member denial, repeat seed import, history after edits/deletion | None yet |
| US-W01 | Three goals, invalid/empty goal, insufficient exercises, refresh, another user's plan | None yet |
| US-W04 | Success, retries, concurrency, invalid dates, transaction failure | None yet |
| US-S01 | Duplicate/consecutive/missed dates, midnight, no activity yet today | None yet |
| Regression | Authentication/health still pass, migration preserves old data | None yet |

- [ ] Apply the [shared Definition of Done](../PROJECT_SPEC.md#definition-of-done) to each task/story.
- [ ] Demonstrate goal → plan → completion → streak, then retries and invalid input.
- [ ] Explain the rules, sequence diagram, tests, and CI for the demonstrated commit.
- [ ] Record D-04 before including challenges in Sprint 3.
- [ ] Record actual feedback and one improvement for the next sprint.

## Work Log and AI Handover

Use the [shared prompt](../PROJECT_SPEC.md#shared-ai-prompt). No Sprint 2 work session has been confirmed yet.

| Log | Date / member | Task | Result | Commit/PR/test | Reviewer and conclusion |
| --- | --- | --- | --- | --- | --- |
| None yet | To be filled | To be filled | To be filled | To be filled | To be filled |

```text
Log: S2-LOG-[number]
Date, time, and timezone: [actual time]
Member / task / story / issue: [name and IDs]
Starting commit: [commit]
Goal and acceptance criteria: [one outcome and its checks]
AI assistance: [tool/model, request, proposal, or code]
What the member verified or changed: [specific details]
Changed files: [relative paths]
Commands/checks executed and results: [actual results, or not run]
Evidence / PR: [link, or unavailable]
Reviewer and conclusion: [name/conclusion, or awaiting review]
Blockers / next steps: [details]
```

## Revision History

| Version | Date | Change | Confirmation |
| --- | --- | --- | --- |
| 0.1 | 19 November 2026 | Expand WBS 2.1–2.8, retaining story IDs from the execution guide | Draft prepared with AI, awaiting team confirmation |
| 0.2 | 19 November 2026 | Translate into English and update navigation links | Awaiting team review |
| 0.3 | 20 November 2026 | Synchronize named owners and reviewers with the main specification roster | Names supplied by the user; task acknowledgements and reviews pending |
