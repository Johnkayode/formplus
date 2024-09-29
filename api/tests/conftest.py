import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

@pytest.fixture(scope="session")
def database():
    db.create_all()  
    yield db
    db.drop_all()