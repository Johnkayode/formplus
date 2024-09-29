import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client
