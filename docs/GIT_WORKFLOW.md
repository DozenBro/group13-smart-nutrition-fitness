# Git Workflow

**Group 13 · Smart Nutrition & Fitness · 20 November 2026**

Use this guide when contributing code, tests, specifications, or other project files. Commands below use Windows PowerShell and run from the repository root unless stated otherwise.

**Task → update main → create a branch → implement and test → commit and push → open a PR → review → merge → update the task.**

## Quick Reference

| Term | Meaning |
| --- | --- |
| `main` | The shared, integrated version of the project |
| Branch | A separate line of work for one task |
| Commit | A saved set of changes in your local Git history |
| Push | Upload local commits to GitHub |
| Pull request (PR) | A request to review and merge your branch into `main` |
| Merge | Combine the reviewed changes with the shared version |
| Conflict | Overlapping changes that need a person to resolve |

## 1. Set Up Once

Accept the repository invitation using your own GitHub account. Install Git, then clone the repository into a folder you choose:

```powershell
git clone https://github.com/DozenBro/group13-smart-nutrition-fitness.git
cd group13-smart-nutrition-fitness
```

If you already have a Git checkout, open that folder instead of cloning again.

Configure your own author identity for this repository. Replace both example values; use an email associated with your GitHub account, including its GitHub-provided private email if preferred.

```powershell
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
git config --get user.name
git config --get user.email
```

Follow the [README](../README.md#installation) to install the application dependencies.

## 2. Take a Task

Read the [main specification](PROJECT_SPEC.md) and the relevant [Sprint 1](sprints/SPRINT_1.md), [Sprint 2](sprints/SPRINT_2.md), or [Sprint 3](sprints/SPRINT_3.md) specification.

Create or link an issue containing:

- The task ID, such as `S1-07`, and related story IDs.
- The owner and a different member who will review the work.
- The expected result, acceptance criteria, and dependencies.

Tell affected teammates before changing a shared API, schema, business rule, or a file they are also editing. Keep the task status accurate in its issue and sprint records.

## 3. Update Main and Create a Branch

Check the current branch and local changes:

```powershell
git status
```

Continue when the working tree is clean. If there are unfinished changes, save them in a commit on their task branch before switching. If unsure which task they belong to, ask a teammate before proceeding.

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/S1-07-tdee
```

Replace the example branch name with your task. Create the branch once; on later work sessions, switch to the existing branch with `git switch feature/S1-07-tdee`.

| Change | Example branch |
| --- | --- |
| Feature | `feature/S1-04-login` |
| Bug fix | `fix/S1-06-owner-check` |
| Documentation | `docs/S1-01-acceptance-criteria` |

Use one branch per task. Start the next task from an updated `main` after the previous work is merged. If a task depends on an unmerged branch, coordinate that dependency first.

## 4. Implement and Verify

Work in small steps. Update the relevant specification when the agreed behavior changes. Record significant AI assistance and what you personally checked.

Run the checks relevant to your changes. Backend tests run from the repository root:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

For frontend changes:

```powershell
cd frontend
npm run build
cd ..
```

For UI or integrated behavior, also run the application and try the relevant successful and failing user journeys. For documentation-only work, check the content, links, and consistency with the specification.

Record actual results. If a check could not run, state the reason in the PR rather than recording it as passed.

## 5. Commit and Push Your Branch

Review the files and changes:

```powershell
git status
git diff
```

Stage only files belonging to this task. The following is an example for a task that changed these two files; adapt the file list to your actual work, including any new files:

```powershell
git add backend/health.py tests/test_measurements.py
git diff --staged
git commit -m "feat(S1-07): add TDEE calculation"
git push -u origin feature/S1-07-tdee
```

Use a message that describes what the commit actually does. Examples: `fix(S1-06): reject cross-account access` or `docs(S1-01): clarify measurement limits`.

For later changes on the same branch, review, stage, and commit again, then run:

```powershell
git push
```

**A commit stays on your machine until you push it. Pushing a task branch does not merge it into `main`.**

## 6. Open a Pull Request

Open the [repository on GitHub](https://github.com/DozenBro/group13-smart-nutrition-fitness). Create a PR with **base: `main`** and **compare: your task branch**. Check the changed files and request the assigned reviewer's review. Use a Draft PR while the work is unfinished.

Use a clear title, such as `S1-07: Add TDEE calculation`, and this description:

```text
Task / story: [IDs]
Issue: [link or issue number]

Changes:
- [behavior or documentation changed]

Verification:
- [command or manual steps]
- [actual result; include checks not run and why]

Spec / API / database changes:
- [details, or none]

Known issues:
- [details, or none]

AI assistance:
- [what AI helped with and what I personally verified, or none]
```

When addressing feedback, commit and push to the same branch. The existing PR updates automatically.

## 7. Review, Merge, and Close the Task

The reviewer checks the requirements, changed code/docs, relevant failure cases, and verification results. The author answers questions and fixes issues before merging.

Use these team rules:

- At least one other member approves the current changes.
- Required task checks and the GitHub Actions build/test workflow pass.
- Review comments are resolved and the branch has no merge conflicts.
- New changes after approval are reviewed again where they affect the approval.
- Use **Squash and merge** consistently, with the task ID in the final commit title. The author merges only after the review conditions are met; the reviewer can merge instead by agreement.

These are collaboration rules. This guide does not configure GitHub branch protection or automatic enforcement.

After merging, record the PR/commit and actual checks in the sprint log. Mark the task Done only when the [Definition of Done](PROJECT_SPEC.md#definition-of-done) is met; merging alone does not establish acceptance of a complete story.

Before starting another task:

```powershell
git switch main
git pull --ff-only origin main
```

## 8. Bring Main into an Ongoing Task

Use this when `main` has changed and your task branch needs the updated code, especially before final review. Commit your current work and confirm a clean working tree first. Stay on your task branch:

```powershell
git branch --show-current
git fetch origin
git merge --no-edit origin/main
```

If the merge succeeds, rerun affected checks and push the updated branch. Use merging consistently for this beginner workflow so teammates do not need to rewrite shared branch history.

If there is a conflict:

1. Run `git status` to find the affected files.
2. Contact the teammate who changed the overlapping section.
3. Resolve each conflict using the agreed behavior. Review both versions; do not automatically accept every change from one side.
4. Stage the resolved files, finish the merge with `git commit`, rerun affected checks, and push.

If you are unsure, stop and share `git status` and the error with the group. Avoid destructive commands while guessing. If `git pull --ff-only` or a push is rejected, share the error and identify the branch divergence before retrying.

## Shared Rules and AI Handover

- Keep project documentation and code in English. Use each member's own Git/GitHub identity.
- Make team changes through task branches and reviewed PRs. Do not push directly to `main`.
- Keep credentials, `.env`, local database files, and private user data out of commits and AI prompts.
- Do not use `push --force`, `reset --hard`, or delete another member's branch without coordinated review of the consequences.
- When stuck, share the task ID, branch, command, exact error, and expected result. Remove credentials first.

Give an AI assistant this context before it edits files:

```text
Read docs/PROJECT_SPEC.md, the relevant sprint specification, and docs/GIT_WORKFLOW.md.
My name / role: [from the main roster]
Task / issue / acceptance criteria: [IDs, links, and expected outcomes]
Current branch / starting commit: [actual values]
Work only on this task branch. Preserve unrelated changes.
Explain each change and how I can verify it. Flag missing decisions.
Before committing, show the changed files and actual verification results.
Push only to the task branch when authorized. Do not merge or push to main.
At handover, summarize changes, AI assistance, checks, blockers, and next steps.
```

References: [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow), [Git pull](https://git-scm.com/docs/git-pull), and [Git merge](https://git-scm.com/docs/git-merge).
