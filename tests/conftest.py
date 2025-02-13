import pytest
from app import create_app, db


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("config.TestingConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()

   # insert data in db

    db.session.commit()

    yield

    db.drop_all()
