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
    # Create form
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()

    # update created forn
    id = data["_id"]
    data["title"] = "Updated Form"
    response = client.put(f'/forms/{id}', json=data)
    data = response.get_json()
    assert response.status_code == 200
    assert data["title"] == "Updated Form"


def test_submit_closed_form(client):
    # create closed form
    f = open('tests/payload.json')
    data = json.load(f)
    data["is_open"] = False
    response = client.post('/forms', json=data)
    data = response.get_json()

    # submit forn
    submission_data = {
        "sections": {
            data["sections"][0]["id"]: {
                data["sections"][0]["fields"][0]["id"]: "Jane",
                data["sections"][0]["fields"][1]["id"]: "Doe",
                data["sections"][0]["fields"][2]["id"]: 1
            }
        }
    }
    
    id = data["_id"]
    response = client.post(f'/forms/{id}/submit', json=submission_data)
    data = response.get_json()
    assert response.status_code == 400
    assert data["message"] == "Form is not open to submissions."


def test_submit_valid_form(client):
    # create form
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()

    # submit forn
    submission_data = {
        "sections": {
            data["sections"][0]["id"]: {
                data["sections"][0]["fields"][0]["id"]: "Jane",
                data["sections"][0]["fields"][1]["id"]: "Doe",
                data["sections"][0]["fields"][2]["id"]: 1
            }
        }
    }
    
    id = data["_id"]
    response = client.post(f'/forms/{id}/submit', json=submission_data)
    data = response.get_json()
    assert response.status_code == 201
    assert data["form_id"] == id


def test_submit_invalid_form(client):
    # create form
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()

    # submit forn with invalid  option
    submission_data = {
        "sections": {
            data["sections"][0]["id"]: {
                data["sections"][0]["fields"][0]["id"]: "John",
                data["sections"][0]["fields"][1]["id"]: "Doe",
                data["sections"][0]["fields"][2]["id"]: 5
            }
        }
    }
    
    id = data["_id"]
    response = client.post(f'/forms/{id}/submit', json=submission_data)
    assert response.status_code == 400


def test_submit_missing_required_fields(client):
    # create form
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()

    # submit forn wiht missing fields
    submission_data = {
        "sections": {
            data["sections"][0]["id"]: {
                data["sections"][0]["fields"][0]["id"]: "Jane",
                data["sections"][0]["fields"][2]["id"]: 1
            }
        }
    }
    
    id = data["_id"]
    response = client.post(f'/forms/{id}/submit', json=submission_data)
    assert response.status_code == 400


def test_retrieve_submissions(client):
    # create form
    f = open('tests/payload.json')
    data = json.load(f)
    response = client.post('/forms', json=data)
    data = response.get_json()

    id = data["_id"]
    response = client.get(f'/forms/{id}/submissions')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["count"] == 0

    # submit forn
    submission_data = {
        "sections": {
            data["sections"][0]["id"]: {
                data["sections"][0]["fields"][0]["id"]: "Dwight",
                data["sections"][0]["fields"][1]["id"]: "Shrute",
                data["sections"][0]["fields"][2]["id"]: 0
            }
        }
    }
    
    id = data["_id"]
    response = client.post(f'/forms/{id}/submit', json=submission_data)
    assert response.status_code == 201

    response = client.get(f'/forms/{id}/submissions')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data["count"] == 1



    