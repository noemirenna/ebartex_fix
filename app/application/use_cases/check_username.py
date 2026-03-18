import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.auth import UsernameAvailabilityResponse
from app.infrastructure.database.repositories import UserRepository

_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


async def check_username_availability(
    session: AsyncSession, raw_username: str
) -> UsernameAvailabilityResponse:
    stripped = (raw_username or "").strip()
    normalized = stripped.lower()

    if not stripped:
        return UsernameAvailabilityResponse(
            available=False,
            normalized_username="",
            valid_format=False,
        )

    if not _USERNAME_PATTERN.match(stripped):
        return UsernameAvailabilityResponse(
            available=False,
            normalized_username=normalized,
            valid_format=False,
        )

    user_repo = UserRepository(session)
    existing = await user_repo.get_by_username(normalized)
    return UsernameAvailabilityResponse(
        available=existing is None,
        normalized_username=normalized,
        valid_format=True,
    )
