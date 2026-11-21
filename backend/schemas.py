from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


ACTIVITY_CODES = (
    'sedentary',
    'lightly_active',
    'moderately_active',
    'active',
    'very_active',
)


def normalize_email(value: str) -> str:
    return value.strip().lower()


class RegisterInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator('email')
    @classmethod
    def _normalize(cls, value: str) -> str:
        return normalize_email(value)


class LoginInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator('email')
    @classmethod
    def _normalize(cls, value: str) -> str:
        return normalize_email(value)


class UserOutput(BaseModel):
    id: int
    email: str
    role: str
    is_locked: bool
    created_at: datetime


class TokenResponse(BaseModel):
    token: str
    expires_at: datetime
    user: UserOutput


class ProfileInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    age_years: int = Field(ge=19, le=78)
    sex_for_equation: str = Field(pattern='^(male|female)$')
    activity_level: str = Field(pattern='^(' + '|'.join(ACTIVITY_CODES) + ')$')


class ProfileOutput(BaseModel):
    user_id: int
    age_years: int | None
    sex_for_equation: str | None
    activity_level: str | None
    updated_at: datetime | None