from fastapi import APIRouter
from sqlalchemy import select

from .dependencies import CurrentUserDependency, SessionDependency
from .models import Profile
from .auth_schemas import ProfileInput, ProfileOutput

router = APIRouter(prefix='/api/profile', tags=['profile'])


def _profile_output(profile: Profile | None, user_id: int) -> ProfileOutput:
    if profile is None:
        return ProfileOutput(
            user_id=user_id,
            age_years=None,
            sex_for_equation=None,
            activity_level=None,
            updated_at=None,
        )
    return ProfileOutput(
        user_id=profile.user_id,
        age_years=profile.age_years,
        sex_for_equation=profile.sex_for_equation,
        activity_level=profile.activity_level,
        updated_at=profile.updated_at,
    )


@router.get('', response_model=ProfileOutput)
def get_profile(user: CurrentUserDependency, session: SessionDependency):
    profile = session.get(Profile, user.id)
    return _profile_output(profile, user.id)


@router.put('', response_model=ProfileOutput)
def put_profile(
    data: ProfileInput,
    user: CurrentUserDependency,
    session: SessionDependency,
):
    profile = session.get(Profile, user.id)
    if profile is None:
        profile = Profile(user_id=user.id)
        session.add(profile)
    profile.age_years = data.age_years
    profile.sex_for_equation = data.sex_for_equation
    profile.activity_level = data.activity_level
    session.commit()
    session.refresh(profile)
    return _profile_output(profile, user.id)