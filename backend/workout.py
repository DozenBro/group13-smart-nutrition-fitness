from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

ACTIVITY_TZ = timezone(timedelta(hours=7))


def activity_today(now: datetime | None = None) -> date:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('now must be timezone-aware.')
    return now.astimezone(ACTIVITY_TZ).date()


def calculate_streak(active_dates: Iterable[date], today: date) -> int:
    days = {d for d in active_dates if d <= today}
    if today in days:
        cursor = today
    elif today - timedelta(days=1) in days:
        cursor = today - timedelta(days=1)
    else:
        return 0
    streak = 0
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


@dataclass(frozen=True)
class PlanTemplate:
    days: tuple[int, ...]
    exercises_per_session: int
    sets: int
    reps: int
    duration_seconds: int
    rest_seconds: int
    description: str


TEMPLATES: dict[str, PlanTemplate] = {
    'weight_loss': PlanTemplate((1, 3, 5, 6), 5, 3, 15, 40, 30, '4 sessions/week, 5 exercises, 3 sets of 15 reps or 40 s, 30 s rest.'),
    'muscle_gain': PlanTemplate((1, 2, 4, 5), 6, 4, 8, 30, 90, '4 sessions/week, 6 exercises, 4 sets of 8 reps or 30 s, 90 s rest.'),
    'maintenance': PlanTemplate((1, 3, 5), 5, 3, 12, 30, 60, '3 sessions/week, 5 exercises, 3 sets of 12 reps or 30 s, 60 s rest.'),
}
GOALS = tuple(TEMPLATES)
SELECTION_RULE = 'Interleave approved exercises across categories to balance sessions and catalog rotation.'


class InsufficientExercisesError(Exception):
    def __init__(self, goal: str, needed: int, found: int):
        self.goal, self.needed, self.found = goal, needed, found
        super().__init__(f'Not enough approved exercises for {goal}: need at least {needed}, found {found}.')


@dataclass(frozen=True)
class ExerciseCandidate:
    id: int
    name: str
    category: str
    activity_unit: str
    instructions: str
    goal_tags: frozenset[str]


@dataclass(frozen=True)
class ItemDraft:
    position: int
    exercise_id: int
    exercise_name: str
    instructions: str
    sets: int
    reps: int | None
    duration_seconds: int | None
    rest_seconds: int


@dataclass(frozen=True)
class SessionDraft:
    day_number: int
    title: str
    items: tuple[ItemDraft, ...]


def interleave_by_category(candidates: Iterable[ExerciseCandidate]) -> list[ExerciseCandidate]:
    groups: dict[str, list[ExerciseCandidate]] = {}
    for c in sorted(candidates, key=lambda x: (x.category.casefold(), x.name.casefold(), x.id)):
        groups.setdefault(c.category, []).append(c)
    queues, result = list(groups.values()), []
    while any(queues):
        for q in queues:
            if q:
                result.append(q.pop(0))
    return result


def build_plan(goal: str, exercises: Iterable[ExerciseCandidate]) -> list[SessionDraft]:
    template = TEMPLATES.get(goal)
    if not template:
        raise ValueError(f'Unknown goal: {goal!r}.')
    pool = interleave_by_category(e for e in exercises if goal in e.goal_tags)
    n = template.exercises_per_session
    if len(pool) < n:
        raise InsufficientExercisesError(goal, n, len(pool))

    sessions = []
    for idx, day in enumerate(template.days):
        items = []
        for pos in range(n):
            ex = pool[(idx * n + pos) % len(pool)]
            by_time = ex.activity_unit == 'seconds'
            items.append(ItemDraft(
                position=pos + 1, exercise_id=ex.id, exercise_name=ex.name, instructions=ex.instructions,
                sets=template.sets, reps=None if by_time else template.reps,
                duration_seconds=template.duration_seconds if by_time else None, rest_seconds=template.rest_seconds,
            ))
        sessions.append(SessionDraft(day_number=day, title=f'Session {idx + 1}', items=tuple(items)))
    return sessions
