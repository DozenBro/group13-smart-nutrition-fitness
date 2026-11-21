from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from .database import get_session
from .models import (
    Exercise, ExerciseCategory, PlanItem, WorkoutLog, WorkoutPlan, WorkoutSession,
)
from .schemas.workout import (
    CategoryInput, CategoryOutput, CompletionOutput, Difficulty, ExerciseImport,
    ExerciseInput, ExerciseOutput, Goal, PlanInput, PlanItemOutput, PlanOutput,
    SessionOutput, StreakOutput,
)
from .workout import (
    SELECTION_RULE, TEMPLATES, ExerciseCandidate, InsufficientExercisesError,
    activity_today, build_plan, calculate_streak,
)

router = APIRouter(prefix='/api')
SessionDependency = Annotated[Session, Depends(get_session)]


def current_user_id(x_user_id: Annotated[int | None, Header()] = None) -> int:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail='Authentication required.')
    return x_user_id


def require_admin(
    user_id: Annotated[int, Depends(current_user_id)],
    x_user_role: Annotated[str | None, Header()] = None,
) -> int:
    if x_user_role != 'admin':
        raise HTTPException(status_code=403, detail='Administrator access required.')
    return user_id


def get_today() -> date:
    return activity_today()


CurrentUser = Annotated[int, Depends(current_user_id)]
AdminUser = Annotated[int, Depends(require_admin)]
Today = Annotated[date, Depends(get_today)]


def exercise_output(row: Exercise) -> ExerciseOutput:
    return ExerciseOutput(
        id=row.id, name=row.name, category=row.category.name, equipment=row.equipment,
        difficulty=row.difficulty, instructions=row.instructions, activity_unit=row.activity_unit,
        goal_tags=[t for t in row.goal_tags.split(',') if t],
        source=row.source, review_status=row.review_status, is_active=row.is_active,
    )


def plan_output(plan: WorkoutPlan, completed_ids: set[int]) -> PlanOutput:
    return PlanOutput(
        id=plan.id, goal=plan.goal, status=plan.status, created_at=plan.created_at,
        template=TEMPLATES[plan.goal].description, selection_rule=SELECTION_RULE,
        sessions=[
            SessionOutput(
                id=s.id, day_number=s.day_number, title=s.title,
                completed=s.id in completed_ids,
                items=[PlanItemOutput(
                    position=i.position, exercise_id=i.exercise_id,
                    exercise_name=i.exercise_name, instructions=i.instructions,
                    sets=i.sets, reps=i.reps, duration_seconds=i.duration_seconds,
                    rest_seconds=i.rest_seconds,
                ) for i in s.items],
            ) for s in plan.sessions
        ],
    )


def tags_to_text(tags: list[str]) -> str:
    return ','.join(sorted(set(tags)))


def active_category(session: Session, name: str) -> ExerciseCategory | None:
    return session.scalar(select(ExerciseCategory).where(
        ExerciseCategory.name == name, ExerciseCategory.is_active.is_(True)))


def get_exercise_or_404(session: Session, exercise_id: int) -> Exercise:
    row = session.get(Exercise, exercise_id)
    if not row:
        raise HTTPException(status_code=404, detail='Exercise not found.')
    return row


def commit_or_conflict(session: Session, detail: str) -> None:
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail=detail)


@router.get('/exercise-categories', response_model=list[CategoryOutput])
def list_categories(session: SessionDependency, user_id: CurrentUser):
    query = select(ExerciseCategory).where(ExerciseCategory.is_active.is_(True)).order_by(ExerciseCategory.name.asc())
    return list(session.scalars(query))


@router.post('/admin/exercise-categories', response_model=CategoryOutput, status_code=201)
def create_category(data: CategoryInput, session: SessionDependency, admin: AdminUser):
    row = ExerciseCategory(name=data.name)
    session.add(row)
    commit_or_conflict(session, 'A category with this name already exists.')
    session.refresh(row)
    return row


@router.put('/admin/exercise-categories/{category_id}', response_model=CategoryOutput)
def rename_category(category_id: int, data: CategoryInput, session: SessionDependency, admin: AdminUser):
    row = session.get(ExerciseCategory, category_id)
    if not row or not row.is_active:
        raise HTTPException(status_code=404, detail='Category not found.')
    row.name = data.name
    commit_or_conflict(session, 'A category with this name already exists.')
    session.refresh(row)
    return row


@router.delete('/admin/exercise-categories/{category_id}', status_code=204)
def archive_category(category_id: int, session: SessionDependency, admin: AdminUser):
    row = session.get(ExerciseCategory, category_id)
    if not row or not row.is_active:
        raise HTTPException(status_code=404, detail='Category not found.')
    in_use = session.scalar(select(Exercise.id).where(
        Exercise.category_id == row.id, Exercise.is_active.is_(True)).limit(1))
    if in_use is not None:
        raise HTTPException(status_code=409, detail='Archive or move the active exercises in this category first.')
    row.is_active = False
    session.commit()


@router.get('/exercises', response_model=list[ExerciseOutput])
def list_exercises(
    session: SessionDependency, user_id: CurrentUser,
    category: Annotated[str | None, Query(max_length=100)] = None,
    difficulty: Difficulty | None = None,
    goal: Goal | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    query = select(Exercise).join(ExerciseCategory).where(
        Exercise.is_active.is_(True), Exercise.review_status == 'approved',
        ExerciseCategory.is_active.is_(True))
    if category:
        query = query.where(ExerciseCategory.name == category)
    if difficulty:
        query = query.where(Exercise.difficulty == difficulty)
    rows = session.scalars(query.order_by(Exercise.name.asc(), Exercise.id.asc()).limit(limit))
    result = [exercise_output(r) for r in rows]
    return [r for r in result if goal in r.goal_tags] if goal else result


@router.get('/admin/exercises', response_model=list[ExerciseOutput])
def admin_list_exercises(
    session: SessionDependency, admin: AdminUser,
    include_archived: bool = False,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    query = select(Exercise)
    if not include_archived:
        query = query.where(Exercise.is_active.is_(True))
    rows = session.scalars(query.order_by(Exercise.name.asc(), Exercise.id.asc()).limit(limit))
    return [exercise_output(r) for r in rows]


@router.post('/admin/exercises', response_model=ExerciseOutput, status_code=201)
def create_exercise(data: ExerciseInput, session: SessionDependency, admin: AdminUser):
    category = active_category(session, data.category)
    if not category:
        raise HTTPException(status_code=422, detail=f'Unknown category: {data.category}.')
    row = Exercise(
        name=data.name, category_id=category.id, equipment=data.equipment,
        difficulty=data.difficulty, instructions=data.instructions,
        activity_unit=data.activity_unit, goal_tags=tags_to_text(data.goal_tags),
        source=data.source, review_status=data.review_status,
    )
    session.add(row)
    commit_or_conflict(session, 'An exercise with this name already exists.')
    session.refresh(row)
    return exercise_output(row)


@router.put('/admin/exercises/{exercise_id}', response_model=ExerciseOutput)
def update_exercise(exercise_id: int, data: ExerciseInput, session: SessionDependency, admin: AdminUser):
    row = get_exercise_or_404(session, exercise_id)
    category = active_category(session, data.category)
    if not category:
        raise HTTPException(status_code=422, detail=f'Unknown category: {data.category}.')
    row.name, row.category_id, row.equipment = data.name, category.id, data.equipment
    row.difficulty, row.instructions = data.difficulty, data.instructions
    row.activity_unit, row.goal_tags = data.activity_unit, tags_to_text(data.goal_tags)
    row.source, row.review_status = data.source, data.review_status
    commit_or_conflict(session, 'An exercise with this name already exists.')
    session.refresh(row)
    return exercise_output(row)


@router.delete('/admin/exercises/{exercise_id}', status_code=204)
def archive_exercise(exercise_id: int, session: SessionDependency, admin: AdminUser):
    row = get_exercise_or_404(session, exercise_id)
    if not row.is_active:
        raise HTTPException(status_code=404, detail='Exercise not found.')
    row.is_active = False
    session.commit()


@router.post('/admin/exercises/import')
def import_exercises(data: ExerciseImport, session: SessionDependency, admin: AdminUser):
    existing = set(session.scalars(select(Exercise.name)))
    categories = {c.name: c for c in session.scalars(select(ExerciseCategory))}
    created = skipped = 0
    for item in data.exercises:
        if item.name in existing:
            skipped += 1
            continue
        category = categories.get(item.category)
        if category is None:
            category = ExerciseCategory(name=item.category)
            session.add(category)
            session.flush()
            categories[item.category] = category
        session.add(Exercise(
            name=item.name, category_id=category.id, equipment=item.equipment,
            difficulty=item.difficulty, instructions=item.instructions,
            activity_unit=item.activity_unit, goal_tags=tags_to_text(item.goal_tags),
            source=item.source, review_status=item.review_status,
        ))
        existing.add(item.name)
        created += 1
    commit_or_conflict(session, 'Import conflicted with a concurrent change. Please retry.')
    return {'created': created, 'skipped': skipped}


def load_plan(session: Session, **filters) -> WorkoutPlan | None:
    query = select(WorkoutPlan).options(selectinload(WorkoutPlan.sessions).selectinload(WorkoutSession.items))
    for column, value in filters.items():
        query = query.where(getattr(WorkoutPlan, column) == value)
    return session.scalar(query.order_by(WorkoutPlan.id.desc()).limit(1))


def completed_session_ids(session: Session, user_id: int, plan: WorkoutPlan) -> set[int]:
    ids = [s.id for s in plan.sessions]
    if not ids:
        return set()
    return set(session.scalars(select(WorkoutLog.session_id).where(
        WorkoutLog.user_id == user_id, WorkoutLog.session_id.in_(ids))))


@router.post('/workout-plans', response_model=PlanOutput, status_code=201)
def create_plan(data: PlanInput, session: SessionDependency, user_id: CurrentUser):
    rows = session.scalars(
        select(Exercise).join(ExerciseCategory).where(
            Exercise.is_active.is_(True), Exercise.review_status == 'approved',
            ExerciseCategory.is_active.is_(True)))
    candidates = [
        ExerciseCandidate(
            id=r.id, name=r.name, category=r.category.name, activity_unit=r.activity_unit,
            instructions=r.instructions, goal_tags=frozenset(t for t in r.goal_tags.split(',') if t))
        for r in rows
    ]
    try:
        drafts = build_plan(data.goal, candidates)
    except InsufficientExercisesError as error:
        raise HTTPException(status_code=422, detail=str(error))

    for old in session.scalars(select(WorkoutPlan).where(WorkoutPlan.user_id == user_id, WorkoutPlan.status == 'active')):
        old.status = 'archived'
    session.flush()

    plan = WorkoutPlan(user_id=user_id, goal=data.goal, status='active')
    for draft in drafts:
        session_row = WorkoutSession(day_number=draft.day_number, title=draft.title)
        session_row.items = [PlanItem(
            position=i.position, exercise_id=i.exercise_id, exercise_name=i.exercise_name,
            instructions=i.instructions, sets=i.sets, reps=i.reps,
            duration_seconds=i.duration_seconds, rest_seconds=i.rest_seconds,
        ) for i in draft.items]
        plan.sessions.append(session_row)
    session.add(plan)
    commit_or_conflict(session, 'Another plan request was in progress. Please try again.')
    return plan_output(load_plan(session, id=plan.id), set())


@router.get('/workout-plans/current', response_model=PlanOutput)
def current_plan(session: SessionDependency, user_id: CurrentUser):
    plan = load_plan(session, user_id=user_id, status='active')
    if not plan:
        raise HTTPException(status_code=404, detail='No active workout plan.')
    return plan_output(plan, completed_session_ids(session, user_id, plan))


@router.get('/workout-plans/{plan_id}', response_model=PlanOutput)
def get_plan(plan_id: int, session: SessionDependency, user_id: CurrentUser):
    plan = load_plan(session, id=plan_id, user_id=user_id)
    if not plan:
        raise HTTPException(status_code=404, detail='Workout plan not found.')
    return plan_output(plan, completed_session_ids(session, user_id, plan))


def user_active_dates(session: Session, user_id: int) -> list[date]:
    return list(session.scalars(select(WorkoutLog.activity_date).where(WorkoutLog.user_id == user_id).distinct()))


@router.post('/workout-sessions/{session_id}/complete', response_model=CompletionOutput, status_code=201)
def complete_session(session_id: int, response: Response, session: SessionDependency, user_id: CurrentUser, today: Today):
    workout_session = session.scalar(
        select(WorkoutSession).join(WorkoutPlan)
        .options(selectinload(WorkoutSession.plan))
        .where(WorkoutSession.id == session_id, WorkoutPlan.user_id == user_id))
    if not workout_session:
        raise HTTPException(status_code=404, detail='Workout session not found.')
    if workout_session.plan.status != 'active':
        raise HTTPException(status_code=409, detail='This plan has been replaced by a newer one.')

    session.add(WorkoutLog(user_id=user_id, session_id=session_id, activity_date=today))
    already = False
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.scalar(select(WorkoutLog).where(
            WorkoutLog.user_id == user_id, WorkoutLog.session_id == session_id))
        if existing is None:
            raise HTTPException(status_code=409, detail='Unable to record the completion.')
        already = True
        response.status_code = 200

    dates = user_active_dates(session, user_id)
    activity_date = session.scalar(select(WorkoutLog.activity_date).where(
        WorkoutLog.user_id == user_id, WorkoutLog.session_id == session_id))
    return CompletionOutput(
        session_id=session_id, activity_date=activity_date, already_completed=already,
        current_streak=calculate_streak(dates, today), active_today=today in dates)


@router.get('/streak', response_model=StreakOutput)
def get_streak(session: SessionDependency, user_id: CurrentUser, today: Today):
    dates = [d for d in user_active_dates(session, user_id) if d <= today]
    return StreakOutput(
        current_streak=calculate_streak(dates, today), active_today=today in dates,
        last_active_date=max(dates) if dates else None, as_of=today)
