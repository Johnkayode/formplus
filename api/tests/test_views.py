import json


def test_create_forms(client):
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    
    assert response.status_code == 201


def test_update_forms(client):
    ...


def test_submit_valid_form():
    ...


def test_submit_invalid_form():
    ...


def test_submit_missing_required_fields():
    ...


def test_retrieve_submissions():
    ...



    