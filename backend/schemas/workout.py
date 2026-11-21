from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Goal = Literal['weight_loss', 'muscle_gain', 'maintenance']
Difficulty = Literal['beginner', 'intermediate', 'advanced']
Unit = Literal['reps', 'seconds']
ReviewStatus = Literal['pending', 'approved']


def short_text(max_length: int):
    return Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=max_length)]


class CategoryInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: short_text(100)


class CategoryOutput(BaseModel):
    id: int
    name: str
    is_active: bool


class ExerciseInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: short_text(150)
    category: short_text(100)
    equipment: short_text(100)
    difficulty: Difficulty
    instructions: short_text(5000)
    activity_unit: Unit
    goal_tags: list[Goal] = Field(min_length=1)
    source: short_text(255)
    review_status: ReviewStatus = 'pending'


class ExerciseImport(BaseModel):
    model_config = ConfigDict(extra='forbid')
    exercises: list[ExerciseInput] = Field(min_length=1, max_length=200)


class ExerciseOutput(BaseModel):
    id: int
    name: str
    category: str
    equipment: str
    difficulty: str
    instructions: str
    activity_unit: str
    goal_tags: list[str]
    source: str
    review_status: str
    is_active: bool


class PlanInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    goal: Goal


class PlanItemOutput(BaseModel):
    position: int
    exercise_id: int
    exercise_name: str
    instructions: str
    sets: int
    reps: int | None
    duration_seconds: int | None
    rest_seconds: int


class SessionOutput(BaseModel):
    id: int
    day_number: int
    title: str
    completed: bool
    items: list[PlanItemOutput]


class PlanOutput(BaseModel):
    id: int
    goal: str
    status: str
    created_at: datetime
    template: str
    selection_rule: str
    sessions: list[SessionOutput]


class CompletionOutput(BaseModel):
    session_id: int
    activity_date: date
    already_completed: bool
    current_streak: int
    active_today: bool


class StreakOutput(BaseModel):
    current_streak: int
    active_today: bool
    last_active_date: date | None
    as_of: date
