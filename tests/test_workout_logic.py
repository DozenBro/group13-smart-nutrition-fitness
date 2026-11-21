from datetime import date, datetime, timedelta, timezone

import pytest

from backend.workout import (
    TEMPLATES, ExerciseCandidate, InsufficientExercisesError, activity_today,
    build_plan, calculate_streak,
)

TODAY = date(2026, 11, 20)
day = lambda offset: TODAY + timedelta(days=offset)


@pytest.mark.parametrize('dates,expected', [
    ([], 0),
    ([TODAY], 1),
    ([TODAY, TODAY, TODAY], 1),
    ([day(-2), day(-1), TODAY], 3),
    ([day(-2), day(-1)], 2),
    ([day(-3), day(-2)], 0),
    ([day(-5), day(-4), day(-3), TODAY], 1),
    ([day(-4), day(-3), day(-1), TODAY], 2),
    ([day(1), day(2)], 0),
])
def test_calculate_streak(dates, expected):
    assert calculate_streak(dates, TODAY) == expected


def test_activity_today():
    assert activity_today(datetime(2026, 11, 20, 16, 59, 59, tzinfo=timezone.utc)) == date(2026, 11, 20)
    assert activity_today(datetime(2026, 11, 20, 17, 0, 0, tzinfo=timezone.utc)) == date(2026, 11, 21)
    with pytest.raises(ValueError):
        activity_today(datetime(2026, 11, 20, 12, 0, 0))


def catalog(count=12, tags=frozenset(TEMPLATES)):
    return [
        ExerciseCandidate(
            id=i + 1, name=f'Exercise {i:02d}', category=['Strength', 'Cardio', 'Core'][i % 3],
            activity_unit='seconds' if i % 2 else 'reps', instructions='Do it.', goal_tags=tags)
        for i in range(count)
    ]


@pytest.mark.parametrize('goal', list(TEMPLATES))
def test_plan_matches_template(goal):
    template = TEMPLATES[goal]
    sessions = build_plan(goal, catalog())
    assert [s.day_number for s in sessions] == list(template.days)
    for s in sessions:
        assert len(s.items) == template.exercises_per_session
        assert len({i.exercise_id for i in s.items}) == template.exercises_per_session
        for i in s.items:
            assert i.sets == template.sets and i.rest_seconds == template.rest_seconds
            assert (i.reps is None) != (i.duration_seconds is None)


def test_plan_units_and_determinism():
    plan = build_plan('maintenance', catalog())
    by_id = {e.id: e for e in catalog()}
    for item in [i for s in plan for i in s.items]:
        if by_id[item.exercise_id].activity_unit == 'seconds':
            assert item.duration_seconds == TEMPLATES['maintenance'].duration_seconds and item.reps is None
        else:
            assert item.reps == TEMPLATES['maintenance'].reps and item.duration_seconds is None
    assert build_plan('weight_loss', catalog()) == build_plan('weight_loss', list(reversed(catalog())))


def test_goal_filtering_and_errors():
    mixed = catalog(6, frozenset({'weight_loss'})) + [
        ExerciseCandidate(100 + i, f'Other {i}', 'Core', 'reps', 'x', frozenset({'muscle_gain'}))
        for i in range(10)
    ]
    used = {i.exercise_id for s in build_plan('weight_loss', mixed) for i in s.items}
    assert used and all(i <= 6 for i in used)
    with pytest.raises(InsufficientExercisesError):
        build_plan('muscle_gain', catalog(5))
    with pytest.raises(ValueError):
        build_plan('unknown_goal', catalog())
