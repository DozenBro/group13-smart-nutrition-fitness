import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from backend.database import SessionLocal
from backend.main import app
from backend.models import Food
from backend.seed_foods import SAMPLE_FOODS, seed_foods


@pytest.fixture(autouse=True)
def clean_foods_table():
    with SessionLocal() as db:
        db.execute(delete(Food))
        db.commit()
    yield
    with SessionLocal() as db:
        db.execute(delete(Food))
        db.commit()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def sample_payload(**overrides):
    data = {
        'name': 'Bún chả Hà Nội (Hanoi Grilled Pork Noodles)',
        'portion_desc': '1 standard serving (~400g)',
        'calories': 520.0,
        'protein_g': 26.0,
        'carbs_g': 64.0,
        'fat_g': 17.5,
        'price_vnd': 45000,
        'meal_slot': 'lunch,dinner',
        'preference_tags': 'traditional',
        'nutrition_source': 'Vietnam National Institute of Nutrition (NIN)',
        'price_source': 'Hanoi local restaurant 2026',
    }
    data.update(overrides)
    return data


def test_create_and_list_foods(client):
    res = client.post('/api/foods', json=sample_payload())
    assert res.status_code == 201
    created = res.json()
    assert created['name'] == 'Bún chả Hà Nội (Hanoi Grilled Pork Noodles)'
    assert created['is_active'] is True

    list_res = client.get('/api/foods')
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) == 1
    assert items[0]['id'] == created['id']


def test_duplicate_food_name_rejected(client):
    payload = sample_payload()
    assert client.post('/api/foods', json=payload).status_code == 201
    dup_res = client.post('/api/foods', json=payload)
    assert dup_res.status_code == 409


def test_filter_foods_by_slot_price_and_tag(client):
    client.post('/api/foods', json=sample_payload(
        name='Bánh mì trứng (Egg Banh Mi)',
        price_vnd=20000,
        meal_slot='breakfast,snack',
        preference_tags='vegetarian,budget',
    ))
    client.post('/api/foods', json=sample_payload(
        name='Cơm tấm sườn (Broken Rice with Pork)',
        price_vnd=50000,
        meal_slot='lunch,dinner',
        preference_tags='high-calorie',
    ))

    res = client.get('/api/foods', params={
        'meal_slot': 'breakfast',
        'max_price_vnd': 25000,
        'tag': 'budget',
    })
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]['name'] == 'Bánh mì trứng (Egg Banh Mi)'


def test_deactivate_food_hides_from_list_but_preserves_row(client):
    created = client.post('/api/foods', json=sample_payload()).json()
    food_id = created['id']

    del_res = client.delete(f'/api/foods/{food_id}')
    assert del_res.status_code == 204

    assert client.get('/api/foods').json() == []
    assert client.delete(f'/api/foods/{food_id}').status_code == 404

    with SessionLocal() as db:
        row = db.get(Food, food_id)
        assert row is not None
        assert row.is_active is False


def test_seed_foods_is_idempotent():
    first_added = seed_foods()
    second_added = seed_foods()

    assert first_added == len(SAMPLE_FOODS)
    assert second_added == 0