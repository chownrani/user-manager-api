from sqlalchemy import select

from src.app.models.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="rani", password="secret", email="rani@example.com"
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == "rani"))

    assert user.id == 1
    assert user.username == "rani"
    assert user.password == "secret"
    assert user.email == "rani@example.com"
    assert user.created_at == time
    assert user.updated_at == time
