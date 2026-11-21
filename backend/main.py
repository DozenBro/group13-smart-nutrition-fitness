import logging
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .database import get_session
from .health import calculate_bmi
from .models import Food, Measurement, User
from .workout_api import router as workout_router


app = FastAPI(title='Group 13 · Measurement demo', version='0.1.0')
SessionDependency = Annotated[Session, Depends(get_session)]
app.include_router(workout_router)


class MeasurementInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    weight_kg: Decimal = Field(gt=0, le=500, max_digits=5, decimal_places=2)
    height_cm: Decimal = Field(ge=50, le=250, max_digits=5, decimal_places=2)


class MeasurementOutput(BaseModel):
    id: int
    weight_kg: float
    height_cm: float
    bmi: float
    created_at: datetime


def measurement_output(row: Measurement) -> MeasurementOutput:
    return MeasurementOutput(
        id=row.id,
        weight_kg=float(row.weight_kg),
        height_cm=float(row.height_cm),
        bmi=float(calculate_bmi(row.weight_kg, row.height_cm)),
        created_at=row.created_at,
    )

# Schema & Mapper
class FoodInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, max_length=150)
    portion_desc: str = Field(min_length=1, max_length=100)
    calories: Decimal = Field(ge=0, max_digits=7, decimal_places=2)
    protein_g: Decimal = Field(ge=0, max_digits=6, decimal_places=2)
    carbs_g: Decimal = Field(ge=0, max_digits=6, decimal_places=2)
    fat_g: Decimal = Field(ge=0, max_digits=6, decimal_places=2)
    price_vnd: int = Field(ge=0)
    meal_slot: str = Field(min_length=1, max_length=50)
    preference_tags: str | None = Field(default=None, max_length=500)
    nutrition_source: str = Field(min_length=1, max_length=255)
    price_source: str = Field(min_length=1, max_length=255)


class FoodOutput(BaseModel):
    id: int
    name: str
    portion_desc: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    price_vnd: int
    meal_slot: str
    preference_tags: str | None
    nutrition_source: str
    price_source: str
    is_active: bool
    created_at: datetime


def food_output(row: Food) -> FoodOutput:
    return FoodOutput(
        id=row.id,
        name=row.name,
        portion_desc=row.portion_desc,
        calories=float(row.calories),
        protein_g=float(row.protein_g),
        carbs_g=float(row.carbs_g),
        fat_g=float(row.fat_g),
        price_vnd=row.price_vnd,
        meal_slot=row.meal_slot,
        preference_tags=row.preference_tags,
        nutrition_source=row.nutrition_source,
        price_source=row.price_source,
        is_active=row.is_active,
        created_at=row.created_at,
    )



@app.exception_handler(SQLAlchemyError)
async def database_error(request, error):
    logging.getLogger(__name__).error('Database operation failed (%s)', type(error).__name__)
    return JSONResponse(status_code=503, content={
        'detail': 'Unable to connect to the database. Please try again later.'
    })


@app.get('/api/measurements', response_model=list[MeasurementOutput])
def list_measurements(
    session: SessionDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
):
    query = select(Measurement).order_by(
        Measurement.created_at.desc(), Measurement.id.desc()
    ).limit(limit)
    return [measurement_output(row) for row in session.scalars(query)]


@app.post('/api/measurements', response_model=MeasurementOutput, status_code=201)
def create_measurement(data: MeasurementInput, session: SessionDependency):
    # S1-03 bridge: until S1-06 wires authenticated identity, attribute
    # new measurements to the Demo User created by the migration.
    demo_user = session.scalar(select(User).where(User.email == 'demo@example.com'))
    if demo_user is None:
        raise HTTPException(500, 'Demo user missing; migration may not have run.')
    row = Measurement(
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        user_id=demo_user.id,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return measurement_output(row)

@app.get('/api/foods', response_model=list[FoodOutput])
def list_foods(
    session: SessionDependency,
    meal_slot: Annotated[str | None, Query(max_length=50)] = None,
    max_price_vnd: Annotated[int | None, Query(ge=0)] = None,
    tag: Annotated[str | None, Query(max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    query = select(Food).where(Food.is_active.is_(True))
    if meal_slot:
        query = query.where(Food.meal_slot.ilike(f'%{meal_slot.strip()}%'))
    if max_price_vnd is not None:
        query = query.where(Food.price_vnd <= max_price_vnd)
    if tag:
        query = query.where(Food.preference_tags.ilike(f'%{tag.strip()}%'))
    query = query.order_by(Food.name.asc(), Food.id.asc()).limit(limit)
    return [food_output(row) for row in session.scalars(query)]


@app.post('/api/foods', response_model=FoodOutput, status_code=201)
def create_food(data: FoodInput, session: SessionDependency):
    row = Food(**data.model_dump())
    session.add(row)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail='A food item with this name already exists.')
    session.refresh(row)
    return food_output(row)


@app.delete('/api/foods/{food_id}', status_code=204)
def deactivate_food(food_id: int, session: SessionDependency):
    row = session.get(Food, food_id)
    if not row or not row.is_active:
        raise HTTPException(status_code=404, detail='Food item not found.')
    row.is_active = False
    session.commit()


dist = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'
if (dist / 'assets').exists():
    app.mount('/assets', StaticFiles(directory=dist / 'assets'), name='assets')


@app.get('/', include_in_schema=False)
def home():
    if not (dist / 'index.html').exists():
        raise HTTPException(503, 'Build the frontend first with npm run build.')
    return FileResponse(dist / 'index.html')

