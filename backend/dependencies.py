import hashlib
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_session
from .models import Session as AuthSession, User

bearer = HTTPBearer(auto_error=False)

SessionDependency = Annotated[Session, Depends(get_session)]


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()


def _auth_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired session.',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def get_current_session(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    session: SessionDependency,
) -> AuthSession:
    if credentials is None or not credentials.credentials:
        raise _auth_error()
    row = session.scalar(
        select(AuthSession).where(
            AuthSession.token_hash == hash_token(credentials.credentials)
        )
    )
    if (
        row is None
        or row.revoked_at is not None
        or row.expires_at <= datetime.now(timezone.utc)
    ):
        raise _auth_error()
    return row


CurrentSessionDependency = Annotated[AuthSession, Depends(get_current_session)]


def get_current_user(
    row: CurrentSessionDependency,
    session: SessionDependency,
) -> User:
    user = session.get(User, row.user_id)
    if user is None or user.is_locked:
        raise _auth_error()
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]