# Sprint 3 Vietnamese Meals and Release

**Draft 0.3 · 20 November 2026 · Implementation pending**

Read the [main specification](../PROJECT_SPEC.md), TDEE/ownership in [Sprint 1](SPRINT_1.md), and streak/completion in [Sprint 2](SPRINT_2.md). Scope follows WBS 3.1–3.7. Final acceptance references WBS 4.1–4.2.

## Goal and Dependencies

**Demo flow** — Member has a profile and energy target → enters preferences/budget → receives a meal plan → records completion → activity/streak updates. The complete health → workout → meal flow works on staging.

Reuse Sprint 1 authentication/profile data and Sprint 2 date/streak rules. Data collection and independent meal-algorithm experiments can start early. Names follow the main specification roster. The team must record task acknowledgements, reviewer availability, actual status, and dates below.

| Item | Value |
| --- | --- |
| Start / review date | To be filled |
| Feature freeze / final acceptance deadline | To be filled |
| Staging URL / release commit | Unavailable |
| Coordinator / acceptance tester | To be filled |

## User Stories and Acceptance Criteria

### US-AD03 Manage Vietnamese Foods

**As an Admin, I want to manage foods and nutrition data so that meal suggestions use reliable catalog information.** Owner Thắng, collaborating with Bảo, reviewer Tá Anh. Status Not started. WBS 3.2.

- **AC1** Admins create, read, update, and delete/archive foods according to the agreed history-preservation policy.
- **AC2** Every food includes portion, kcal, protein/carbohydrate/fat, and price in VND on the same portion basis, with nutrition sources and price context.
- **AC3** Missing units or invalid data are rejected. Members calling administration APIs are rejected.
- **AC4** A reviewed seed dataset is available, provisionally 60 foods pending S3-D03. Reimporting it creates no duplicates.
- **AC5** Food edits/deletion preserve the content of previously saved plans.

### US-M01 Obtain and View Meal Suggestions

**As a Member, I want Vietnamese meal suggestions based on energy targets, preferences, and budget so that plans reflect my choices.** Owner Thắng, collaborating with Bảo, reviewer Đạt. Status Not started. WBS 3.3.

- **AC1** Valid inputs and sufficient data produce a plan meeting the agreed calorie, preference, and budget constraints.
- **AC2** Missing target/profile data identifies what to complete. Invalid budgets or preferences are rejected.
- **AC3** If no combination satisfies every constraint, return no-match with guidance on adjusting the request.
- **AC4** Plans display foods, quantities/portions, total kcal, and price, with enough data to explain the selection.
- **AC5** Plans persist after refresh and are accessible only by their owner. Store inputs/rules and necessary food values to preserve history.

### US-M02 Record Meals and Update Activity

**As a Member, I want to mark meals complete so that I can record nutrition habits alongside workouts.** Owners Thắng + Đạt, collaborating with Bảo, reviewer Tuấn Anh. Status Not started. WBS 3.4.

- **AC1** Members complete only meals in their own plans, on permitted dates.
- **AC2** Retries and concurrent requests create one completion for the same meal.
- **AC3** Workouts and meals on one date contribute one day to the combined streak under the agreed rule.
- **AC4** Refresh displays accurate logs and streaks. Save failures do not create false completion states.
- **AC5** If undo is supported, activity is recalculated from remaining valid logs under S2-D03/S3-D02.

### US-C01 Basic Challenges

**As an Admin, I want to manage challenges. As a Member, I want to view my progress against a challenge goal.** Status Awaiting D-04. WBS 3.5. Assign an owner/reviewer if included in the sprint.

- **AC1** Admins manage names, date intervals, and goals. Members access only permitted features.
- **AC2** Progress uses actual logs and does not count the same activity/date twice under the challenge rule.
- **AC3** Members see their own progress and the correct achieved/not-achieved result.

Record the inclusion/deferral decision, decision maker, and reason. If the instructor requires this story, update the plan before acceptance.

## Rules and Decisions

| ID | Decision needed | Owner / status |
| --- | --- | --- |
| S3-D01 | Source of calorie targets, goal adjustments, acceptance of the CSV's ±10% tolerance, and inclusive/exclusive boundaries | Tá Anh + Thắng, awaiting decision |
| S3-D02 | Supported preferences, daily budget, breakfast/lunch/dinner slots, portions, repeated foods, plan replacement, and undo | Thắng + Đạt, awaiting decision |
| S3-D03 | Confirm the damaged symbol before 60, source/portion/price standards, and archiving policy | Tá Anh + Thắng, awaiting decision, provisional target 60 foods |
| S3-D04 | Staging environment, feature-freeze date, UAT scenarios, and acceptance tester | Hưng + Tá Anh, awaiting decision with D-06 |

**Proposed algorithm** — Filter valid foods by preferences and meal slots. Enumerate combinations using agreed portions. Retain combinations within budget and calorie constraints. Rank by smallest target deviation, then lower price, then stable IDs for explainability. Return no-match when no combination qualifies.

Software fixture example, assuming a confirmed target of 2,000 kcal, 10% tolerance, and a 100,000 VND budget. The accepted range is 1,800–2,200 kcal. A preference-compatible combination at 1,950 kcal and 90,000 VND qualifies. A 2,000 kcal combination costing 110,000 VND is rejected. This fixture verifies algorithm constraints.

Continue streak behavior under S2-D03. Changes to shared workout/meal rules require corresponding updates and tests in both modules.

## Design and Data

| Component | Design deliverable |
| --- | --- |
| UI | Preferences, budget, suggested plan, details, no-match, completion, and errors |
| Database | foods, meal_plans, meal_plan_items, meal_logs, and activity/user relationships |
| History | Retain portion/kcal/price values, rules, and inputs needed when creating plans |
| API | Admin foods, plan creation/retrieval, meal completion, and combined streak contracts |
| Integrity | Foreign keys, ownership, unique completions, and consistent log/activity transactions |

Document methods/paths, requests/responses, authentication, and error codes in the design issue before integration. This API group is planned sprint work and awaits implementation.

**Food template** — `id`, Vietnamese name, portion description/weight, kcal, protein/carbohydrate/fat on the same portion basis, VND per portion, meal slot, preference tags, nutrition source, price source/context/date, and reviewer. Label price estimates. Complete missing data or select an appropriately sourced replacement before seeding.

## Tasks and Assignments

| Task | Deliverable | Assigned owner / reviewer | Dependencies | Due | Status | Issue/PR |
| --- | --- | --- | --- | --- | --- | --- |
| S3-01 | Prototype, meal rules, and success/no-match fixtures | Thắng + Bảo / Tá Anh | D-02, S3-D01/S3-D02 | To be filled | Not started | Not created |
| S3-02 | Schema/migration, contracts, food administration, and sourced seed data | Thắng + Tuấn Anh / Đạt | S3-D03 | To be filled | Not started | Not created |
| S3-03 | Recommendation algorithm and saved-plan interface | Thắng + Bảo / Đạt | S3-01, S3-02 data | To be filled | Not started | Not created |
| S3-04 | Meal completion and combined workout/meal streak | Thắng + Đạt / Tuấn Anh | S3-03, Sprint 2 rules | To be filled | Not started | Not created |
| S3-05 | Challenges if confirmed in scope | To be assigned | D-04 | To be filled | Awaiting decision | Not created |
| S3-06 | Regression, authorization, and cross-module error checks | Hưng + whole team / Tuấn Anh | Integrated health/workout/meal flows | To be filled | Not started | Not created |
| S3-07 | Staging, user guide, demo, and release-candidate freeze | Hưng + Tá Anh / Bảo | D-06, S3-D04, S3-06 | To be filled | Not started | Not created |
| S3-08 | Final UAT, defects, tag, and handover documents | Whole team / acceptance tester to be confirmed | Release candidate | To be filled | Not started | Not created |

S3-08 covers final acceptance milestones WBS 4.1–4.2. Schedule these milestones using the actual submission date.

## Testing, Review, and Handover

| Test area | Required cases | Current evidence |
| --- | --- | --- |
| Data | Units/portions, sources, missing fields, negatives, duplicate import, historical price edits | None yet |
| Meal search | Feasible/no-match, invalid preference, missing target, exact budget, and both calorie boundaries | None yet |
| Completion | Success, retries/concurrency, other user, invalid dates, and transaction failures | None yet |
| Combined streak | Workout + meal on one date, meal only, workout only, missed dates, and midnight | None yet |
| Regression | Authentication/health/workout behavior, preserved migration data, and Member/Admin authorization | None yet |
| Release | Fresh setup, staging, persistence after restart, backup/restore, and UAT against criteria | None yet |

- [ ] Meet the [shared Definition of Done](../PROJECT_SPEC.md#definition-of-done) for the agreed scope.
- [ ] Demonstrate health → workout → meal on staging and a no-match case.
- [ ] Review defects, leaving no critical/high defects open under the plan's acceptance criteria.
- [ ] Record the challenge decision, staging URL, commit, and CI/test results.
- [ ] Freeze the release candidate and track subsequent changes through defects/issues.

### Final Acceptance and Submission

- [ ] The acceptance tester executes agreed scenarios and records actual results.
- [ ] Provide a README usable on another machine, user guide, ERD, architecture diagram, and API list matching the code.
- [ ] Provide story → task → commit/PR → test → acceptance-result traceability.
- [ ] Provide sprint reports, feedback, and actual retrospective actions.
- [ ] Record the final tag/commit, backup/restore steps, and disclosed limitations/defects.
- [ ] All six members explain their contributions, AI assistance, and verification performed.

## Work Log and AI Handover

Use the [shared prompt](../PROJECT_SPEC.md#shared-ai-prompt). No Sprint 3 work session has been confirmed yet.

| Log | Date / member | Task | Result | Commit/PR/test | Reviewer and conclusion |
| --- | --- | --- | --- | --- | --- |
| None yet | To be filled | To be filled | To be filled | To be filled | To be filled |

```text
Log: S3-LOG-[number]
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
| 0.1 | 19 November 2026 | Expand WBS 3.1–3.7 and final acceptance WBS 4.1–4.2 | Draft prepared with AI, awaiting team confirmation |
| 0.2 | 19 November 2026 | Translate into English and update navigation links | Awaiting team review |
| 0.3 | 20 November 2026 | Synchronize named owners and reviewers with the main specification roster | Names supplied by the user; task acknowledgements and reviews pending |
