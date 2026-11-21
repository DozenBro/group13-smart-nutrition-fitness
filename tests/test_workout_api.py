from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_session
from backend.main import app
from backend.models import WorkoutLog
from backend.workout_api import get_today

MEMBER = {'X-User-Id': '1'}
OTHER = {'X-User-Id': '2'}
ADMIN = {'X-User-Id': '99', 'X-User-Role': 'admin'}
START = date(2026, 11, 20)


def exercise_payload(i: int, **overrides) -> dict:
    payload = {
        'name': f'Exercise {i:02d}', 'category': ['Strength', 'Cardio', 'Core'][i % 3],
        'equipment': 'none', 'difficulty': 'beginner', 'instructions': 'Do it carefully.',
        'activity_unit': 'seconds' if i % 2 else 'reps',
        'goal_tags': ['weight_loss', 'muscle_gain', 'maintenance'],
        'source': 'unit test', 'review_status': 'approved',
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def client():
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine)
    clock = {'today': START}

    def override_session():
        with factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_today] = lambda: clock['today']
    with TestClient(app) as test_client:
        test_client.clock = clock
        test_client.factory = factory
        yield test_client
    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_today, None)


def seed(client, count=12):
    response = client.post('/api/admin/exercises/import', headers=ADMIN,
                           json={'exercises': [exercise_payload(i) for i in range(count)]})
    assert response.status_code == 200, response.text
    return response.json()


def make_plan(client, goal='weight_loss', headers=MEMBER):
    response = client.post('/api/workout-plans', headers=headers, json={'goal': goal})
    assert response.status_code == 201, response.text
    return response.json()


def next_day(client, days=1):
    client.clock['today'] += timedelta(days=days)


def first_session_id(plan, index=0):
    return plan['sessions'][index]['id']


def complete(client, session_id, headers=MEMBER):
    return client.post(f'/api/workout-sessions/{session_id}/complete', headers=headers)


def log_count(client):
    with client.factory() as session:
        return session.scalar(select(func.count()).select_from(WorkoutLog))


def test_authentication_is_required(client):
    assert client.get('/api/exercises').status_code == 401


def test_member_cannot_use_admin_apis(client):
    assert client.post('/api/admin/exercise-categories', headers=MEMBER, json={'name': 'Cardio'}).status_code == 403
    assert client.post('/api/admin/exercises', headers=MEMBER, json=exercise_payload(0)).status_code == 403
    assert client.get('/api/admin/exercises', headers=MEMBER).status_code == 403
    assert client.post('/api/admin/exercises/import', headers=MEMBER, json={'exercises': [exercise_payload(0)]}).status_code == 403


def test_admin_category_and_exercise_crud(client):
    category = client.post('/api/admin/exercise-categories', headers=ADMIN, json={'name': 'Cardio'})
    assert category.status_code == 201
    assert client.post('/api/admin/exercise-categories', headers=ADMIN, json={'name': 'Cardio'}).status_code == 409

    created = client.post('/api/admin/exercises', headers=ADMIN, json=exercise_payload(0, category='Cardio'))
    assert created.status_code == 201
    exercise_id = created.json()['id']
    assert client.post('/api/admin/exercises', headers=ADMIN, json=exercise_payload(0, category='Cardio')).status_code == 409

    updated = client.put(f'/api/admin/exercises/{exercise_id}', headers=ADMIN, json=exercise_payload(0, category='Cardio', difficulty='advanced'))
    assert updated.status_code == 200 and updated.json()['difficulty'] == 'advanced'

    assert client.delete(f'/api/admin/exercises/{exercise_id}', headers=ADMIN).status_code == 204
    assert client.get('/api/exercises', headers=MEMBER).json() == []
    archived = client.get('/api/admin/exercises?include_archived=true', headers=ADMIN).json()
    assert [e['is_active'] for e in archived] == [False]


def test_exercise_validation(client):
    client.post('/api/admin/exercise-categories', headers=ADMIN, json={'name': 'Cardio'})
    assert client.post('/api/admin/exercises', headers=ADMIN, json=exercise_payload(0, category='Nope')).status_code == 422
    for bad in ({'difficulty': 'impossible'}, {'goal_tags': []}, {'activity_unit': 'miles'}, {'name': '   '}):
        assert client.post('/api/admin/exercises', headers=ADMIN, json=exercise_payload(0, category='Cardio', **bad)).status_code == 422


def test_category_with_active_exercises_cannot_be_archived(client):
    seed(client, 3)
    categories = client.get('/api/exercise-categories', headers=MEMBER).json()
    assert client.delete(f'/api/admin/exercise-categories/{categories[0]["id"]}', headers=ADMIN).status_code == 409


def test_seed_import_is_repeatable(client):
    assert seed(client) == {'created': 12, 'skipped': 0}
    assert seed(client) == {'created': 0, 'skipped': 12}
    assert len(client.get('/api/exercises', headers=MEMBER).json()) == 12


def test_members_only_see_approved_exercises(client):
    client.post('/api/admin/exercises/import', headers=ADMIN, json={'exercises': [
        exercise_payload(0), exercise_payload(1, review_status='pending')]})
    assert [e['name'] for e in client.get('/api/exercises', headers=MEMBER).json()] == ['Exercise 00']


@pytest.mark.parametrize('goal,sessions', [('weight_loss', 4), ('muscle_gain', 4), ('maintenance', 3)])
def test_each_goal_creates_a_valid_plan(client, goal, sessions):
    seed(client)
    plan = make_plan(client, goal)
    assert plan['goal'] == goal and plan['status'] == 'active' and len(plan['sessions']) == sessions
    for session in plan['sessions']:
        assert session['items'] and session['completed'] is False
        for item in session['items']:
            assert item['sets'] > 0 and (item['reps'] is None) != (item['duration_seconds'] is None)


def test_invalid_or_missing_goal_is_rejected(client):
    seed(client)
    for body in ({'goal': 'get_huge'}, {}, {'goal': ''}, {'goal': 'weight_loss', 'extra': 1}):
        assert client.post('/api/workout-plans', headers=MEMBER, json=body).status_code == 422


def test_insufficient_exercises_gives_clear_message(client):
    seed(client, 3)
    response = client.post('/api/workout-plans', headers=MEMBER, json={'goal': 'muscle_gain'})
    assert response.status_code == 422 and 'Not enough approved exercises' in response.json()['detail']


def test_plan_is_saved_and_readable_after_refresh(client):
    seed(client)
    created = make_plan(client)
    current = client.get('/api/workout-plans/current', headers=MEMBER).json()
    assert current == client.get(f'/api/workout-plans/{created["id"]}', headers=MEMBER).json()
    assert current['sessions'] == created['sessions']


def test_only_the_owner_can_read_a_plan(client):
    seed(client)
    plan = make_plan(client)
    assert client.get(f'/api/workout-plans/{plan["id"]}', headers=OTHER).status_code == 404
    assert client.get('/api/workout-plans/current', headers=OTHER).status_code == 404


def test_new_plan_archives_the_previous_one(client):
    seed(client)
    first = make_plan(client, 'weight_loss')
    second = make_plan(client, 'maintenance')
    assert client.get('/api/workout-plans/current', headers=MEMBER).json()['id'] == second['id']
    assert client.get(f'/api/workout-plans/{first["id"]}', headers=MEMBER).json()['status'] == 'archived'


def test_catalog_edits_do_not_change_existing_plans(client):
    seed(client)
    plan = make_plan(client)
    item = plan['sessions'][0]['items'][0]
    exercise = next(e for e in client.get('/api/admin/exercises', headers=ADMIN).json() if e['id'] == item['exercise_id'])
    renamed = {**exercise_payload(0), 'name': 'Renamed exercise', 'category': exercise['category']}
    assert client.put(f'/api/admin/exercises/{exercise["id"]}', headers=ADMIN, json=renamed).status_code == 200
    client.delete(f'/api/admin/exercises/{exercise["id"]}', headers=ADMIN)
    after = client.get('/api/workout-plans/current', headers=MEMBER).json()
    assert after['sessions'][0]['items'][0]['exercise_name'] == item['exercise_name']


def test_completion_is_saved_and_persists(client):
    seed(client)
    plan = make_plan(client)
    response = complete(client, first_session_id(plan))
    assert response.status_code == 201
    body = response.json()
    assert body['already_completed'] is False and body['current_streak'] == 1 and body['activity_date'] == START.isoformat()
    refreshed = client.get('/api/workout-plans/current', headers=MEMBER).json()
    assert [s['completed'] for s in refreshed['sessions']] == [True, False, False, False]


def test_repeat_completion_creates_one_log(client):
    seed(client)
    session_id = first_session_id(make_plan(client))
    first, second, third = (complete(client, session_id) for _ in range(3))
    assert (first.status_code, second.status_code, third.status_code) == (201, 200, 200)
    assert second.json()['already_completed'] is True and second.json()['current_streak'] == 1
    assert log_count(client) == 1


def test_only_the_owner_can_complete_a_session(client):
    seed(client)
    session_id = first_session_id(make_plan(client))
    assert complete(client, session_id, headers=OTHER).status_code == 404
    assert complete(client, 99999).status_code == 404
    assert log_count(client) == 0


def test_cannot_complete_a_session_of_a_replaced_plan(client):
    seed(client)
    old_session = first_session_id(make_plan(client, 'weight_loss'))
    make_plan(client, 'maintenance')
    assert complete(client, old_session).status_code == 409
    assert log_count(client) == 0


def test_save_failure_is_not_reported_as_success(client, monkeypatch):
    seed(client)
    session_id = first_session_id(make_plan(client))

    def broken_commit(self):
        raise OperationalError('COMMIT', {}, Exception('db down'))

    monkeypatch.setattr(Session, 'commit', broken_commit)
    assert complete(client, session_id).status_code == 503
    monkeypatch.undo()
    assert log_count(client) == 0 and client.get('/api/streak', headers=MEMBER).json()['current_streak'] == 0


def test_streak_before_any_activity_is_zero(client):
    assert client.get('/api/streak', headers=MEMBER).json() == {
        'current_streak': 0, 'active_today': False, 'last_active_date': None, 'as_of': START.isoformat(),
    }


def test_two_sessions_on_one_date_count_as_one_day(client):
    seed(client)
    plan = make_plan(client)
    complete(client, first_session_id(plan, 0))
    assert complete(client, first_session_id(plan, 1)).json()['current_streak'] == 1
    assert log_count(client) == 2


def test_streak_across_days_missed_day_and_restart(client):
    seed(client)
    plan = make_plan(client)
    complete(client, first_session_id(plan, 0))
    next_day(client)
    assert complete(client, first_session_id(plan, 1)).json()['current_streak'] == 2

    next_day(client)
    waiting = client.get('/api/streak', headers=MEMBER).json()
    assert waiting['current_streak'] == 2 and waiting['active_today'] is False

    next_day(client, 2)
    assert client.get('/api/streak', headers=MEMBER).json()['current_streak'] == 0
    assert complete(client, first_session_id(plan, 2)).json()['current_streak'] == 1


def test_streak_is_private_to_each_account(client):
    seed(client)
    complete(client, first_session_id(make_plan(client)))
    assert client.get('/api/streak', headers=MEMBER).json()['current_streak'] == 1
    assert client.get('/api/streak', headers=OTHER).json()['current_streak'] == 0


def test_streak_can_be_reconciled_with_logs(client):
    seed(client)
    plan = make_plan(client)
    for index in range(3):
        complete(client, first_session_id(plan, index))
        next_day(client)
    with client.factory() as session:
        dates = set(session.scalars(select(WorkoutLog.activity_date)))
    assert dates == {START, START + timedelta(days=1), START + timedelta(days=2)}
    assert client.get('/api/streak', headers=MEMBER).json()['current_streak'] == 3
