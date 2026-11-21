from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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