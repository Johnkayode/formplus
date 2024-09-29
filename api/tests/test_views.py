import json


def test_create_valid_forms(client):
    """
    Test create valid forms.
    """
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()
    assert response.status_code == 201
    assert data["title"] == "Sample Form"

def test_create_invalid_forms(client):
    """
    Test create valid forms.
    """
    f = open('tests/payload.json')
    data = json.load(f)
    # remove options from the 1st section, 3rd field.
    data["sections"][0]["fields"][2]["options"] = []
    response = client.post('/forms', json=data)
    assert response.status_code == 422


def test_update_forms(client):
    """
    Test update forms sucessfully.
    """
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


def test_submit_closed_form():
    ...

def test_submit_valid_form():
    ...

def test_submit_invalid_form():
    ...


def test_submit_missing_required_fields():
    ...


def test_retrieve_submissions():
    ...



    