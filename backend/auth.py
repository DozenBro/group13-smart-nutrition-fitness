import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .auth_utils import get_password_hash, verify_password
from .dependencies import (
    CurrentSessionDependency,
    CurrentUserDependency,
    SessionDependency,
    hash_token,
)
from .models import Session as AuthSession, User
from .auth_schemas import (
    LoginInput,
    RegisterInput,
    TokenResponse,
    UserOutput,
)

router = APIRouter(prefix='/api/auth', tags=['auth'])

SESSION_LIFETIME = timedelta(days=7)


def _user_output(user: User) -> UserOutput:
    return UserOutput(
        id=user.id,
        email=user.email,
        role=user.role,
        is_locked=user.is_locked,
        created_at=user.created_at,
    )


@router.post('/register', response_model=UserOutput, status_code=201)
def register(data: RegisterInput, session: SessionDependency):
    row = User(
        email=data.email,
        password_hash=get_password_hash(data.password),
        role='member',
        is_locked=False,
    )
    session.add(row)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='An account with this email already exists.',
        )
    session.refresh(row)
    return _user_output(row)


@router.post('/login', response_model=TokenResponse)
def login(data: LoginInput, session: SessionDependency):
    user = session.scalar(select(User).where(User.email == data.email))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials.',
        )
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Account is locked.',
        )
    raw_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + SESSION_LIFETIME
    session.add(AuthSession(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        expires_at=expires_at,
    ))
    session.commit()
    return TokenResponse(
        token=raw_token,
        expires_at=expires_at,
        user=_user_output(user),
    )


@router.post('/logout', status_code=204)
def logout(row: CurrentSessionDependency, session: SessionDependency):
    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        session.commit()


@router.get('/me', response_model=UserOutput)
def me(user: CurrentUserDependency):
    return _user_output(user)