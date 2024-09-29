import json


def test_create_forms(client):
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()
    assert response.status_code == 201
    assert data["title"] == "Sample Form"


def test_update_forms(client):
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()
    id = data["_id"]
    data["title"] = "Updated Form"

    response = client.put(f'/forms/{id}', json=data)
    data = response.get_json()
    assert response.status_code == 200
    assert data["title"] == "Updated Form"



def test_submit_valid_form():
    ...


def test_submit_invalid_form():
    ...


def test_submit_missing_required_fields():
    ...


def test_retrieve_submissions():
    ...



    