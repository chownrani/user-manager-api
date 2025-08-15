import pytest
from sqlalchemy import select

from src.app.models.user import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="rani", password="secret", email="rani@example.com"
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == "rani"))

    assert user.to_dict() == {
        "id": 1,
        "username": "rani",
        "password": "secret",
        "email": "rani@example.com",
        "created_at": time,
        "updated_at": time,
    }
