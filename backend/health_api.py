from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from .dependencies import CurrentUserDependency, SessionDependency
from .health import calculate_bmi, calculate_tdee
from .models import Measurement, Profile

router = APIRouter(prefix='/api/health', tags=['health'])


class EstimateOutput(BaseModel):
    bmi: float | None
    tdee: float | None
    tdee_missing_fields: list[str]
    measurement_id: int | None
    measurement_created_at: datetime | None
    profile_complete: bool


PROFILE_FIELDS = ('age_years', 'sex_for_equation', 'activity_level')


@router.get('/estimate', response_model=EstimateOutput)
def get_estimate(user: CurrentUserDependency, session: SessionDependency):
    latest = session.scalar(
        select(Measurement)
        .where(Measurement.user_id == user.id)
        .order_by(Measurement.created_at.desc(), Measurement.id.desc())
        .limit(1)
    )
    if latest is None:
        return EstimateOutput(
            bmi=None,
            tdee=None,
            tdee_missing_fields=[],
            measurement_id=None,
            measurement_created_at=None,
            profile_complete=False,
        )

    bmi = float(calculate_bmi(latest.weight_kg, latest.height_cm))
    profile = session.get(Profile, user.id)
    missing = [
        f for f in PROFILE_FIELDS
        if profile is None or getattr(profile, f) is None
    ]
    if missing:
        return EstimateOutput(
            bmi=bmi,
            tdee=None,
            tdee_missing_fields=missing,
            measurement_id=latest.id,
            measurement_created_at=latest.created_at,
            profile_complete=False,
        )

    tdee = calculate_tdee(
        weight_kg=latest.weight_kg,
        height_cm=latest.height_cm,
        age_years=profile.age_years,
        sex_for_equation=profile.sex_for_equation,
        activity_level=profile.activity_level,
    )
    return EstimateOutput(
        bmi=bmi,
        tdee=float(tdee),
        tdee_missing_fields=[],
        measurement_id=latest.id,
        measurement_created_at=latest.created_at,
        profile_complete=True,
    )