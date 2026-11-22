from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update

from .dependencies import AdminDependency, SessionDependency
from .models import Session as AuthSession, User
from .auth_schemas import UserOutput

router = APIRouter(prefix='/api/admin', tags=['admin'])


def _output(user: User) -> UserOutput:
    return UserOutput(
        id=user.id,
        email=user.email,
        role=user.role,
        is_locked=user.is_locked,
        created_at=user.created_at,
    )


@router.get('/users', response_model=list[UserOutput])
def list_users(admin: AdminDependency, session: SessionDependency):
    rows = session.scalars(select(User).order_by(User.id.asc()))
    return [_output(u) for u in rows]


@router.post('/users/{user_id}/lock', response_model=UserOutput)
def lock_user(
    user_id: int,
    admin: AdminDependency,
    session: SessionDependency,
):
    target = session.get(User, user_id)
    if target is None:
        raise HTTPException(404, 'User not found.')
    target.is_locked = True
    session.execute(
        update(AuthSession)
        .where(
            AuthSession.user_id == user_id,
            AuthSession.revoked_at.is_(None),
        )
        .values(revoked_at=datetime.now(timezone.utc))
    )
    session.commit()
    session.refresh(target)
    return _output(target)


@router.post('/users/{user_id}/unlock', response_model=UserOutput)
def unlock_user(
    user_id: int,
    admin: AdminDependency,
    session: SessionDependency,
):
    target = session.get(User, user_id)
    if target is None:
        raise HTTPException(404, 'User not found.')
    target.is_locked = False
    session.commit()
    session.refresh(target)
    return _output(target)