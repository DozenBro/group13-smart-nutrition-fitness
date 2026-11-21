from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import select

from .dependencies import CurrentUserDependency, SessionDependency
from .health import calculate_bmi
from .measurement_schemas import MeasurementInput, MeasurementOutput
from .models import Measurement

router = APIRouter(prefix='/api/measurements', tags=['measurements'])


def _output(row: Measurement) -> MeasurementOutput:
    return MeasurementOutput(
        id=row.id,
        weight_kg=float(row.weight_kg),
        height_cm=float(row.height_cm),
        bmi=float(calculate_bmi(row.weight_kg, row.height_cm)),
        created_at=row.created_at,
    )


@router.get('', response_model=list[MeasurementOutput])
def list_measurements(
    user: CurrentUserDependency,
    session: SessionDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
):
    query = (
        select(Measurement)
        .where(Measurement.user_id == user.id)
        .order_by(Measurement.created_at.desc(), Measurement.id.desc())
        .limit(limit)
    )
    return [_output(row) for row in session.scalars(query)]


@router.post('', response_model=MeasurementOutput, status_code=201)
def create_measurement(
    data: MeasurementInput,
    user: CurrentUserDependency,
    session: SessionDependency,
):
    row = Measurement(
        weight_kg=data.weight_kg,
        height_cm=data.height_cm,
        user_id=user.id,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return _output(row)