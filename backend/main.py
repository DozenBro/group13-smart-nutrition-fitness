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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .database import get_session
from .health import calculate_bmi
from .models import Measurement


app = FastAPI(title='Group 13 · Measurement demo', version='0.1.0')
SessionDependency = Annotated[Session, Depends(get_session)]


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


@app.exception_handler(SQLAlchemyError)
async def database_error(request, error):
    logging.getLogger(__name__).error('Database operation failed (%s)', type(error).__name__)
    return JSONResponse(status_code=503, content={
        'detail': 'Chưa kết nối được cơ sở dữ liệu. Hãy thử lại sau.'
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
    row = Measurement(weight_kg=data.weight_kg, height_cm=data.height_cm)
    session.add(row)
    session.commit()
    session.refresh(row)
    return measurement_output(row)


dist = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'
if (dist / 'assets').exists():
    app.mount('/assets', StaticFiles(directory=dist / 'assets'), name='assets')


@app.get('/', include_in_schema=False)
def home():
    if not (dist / 'index.html').exists():
        raise HTTPException(503, 'Build the frontend first with npm run build.')
    return FileResponse(dist / 'index.html')

