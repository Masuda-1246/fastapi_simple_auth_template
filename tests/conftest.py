import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api import deps
from app.db.session import Base

# テスト用のインメモリSQLiteデータベース
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# テスト用のデータベース依存関係をオーバーライド
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# テスト用のDBセッションを提供するための依存関係をオーバーライド
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[deps.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# テスト用のスーパーユーザー
@pytest.fixture(scope="function")
def superuser(db):
    from app.crud.crud_user import user
    from app.schemas.user import UserCreate

    user_in = UserCreate(
        email="admin@example.com",
        password="password",
        full_name="Super User",
        is_superuser=True,
    )
    return user.create(db, obj_in=user_in)


# テスト用の一般ユーザー
@pytest.fixture(scope="function")
def normal_user(db):
    from app.crud.crud_user import user
    from app.schemas.user import UserCreate

    user_in = UserCreate(
        email="user@example.com",
        password="password",
        full_name="Normal User",
        is_superuser=False,
    )
    return user.create(db, obj_in=user_in)
