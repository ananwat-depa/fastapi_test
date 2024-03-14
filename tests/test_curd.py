from fastapi.testclient import TestClient

def test_will_be_a_bug_unless_exist(mock_app):
    with TestClient(mock_app) as client:
        assert True

def test_get(mock_app,mock_database):
    with TestClient(mock_app) as client:
        response = client.get('/users/')
        assert response.status_code == 200
        assert response.json()['user'] == mock_database

def test_post(mock_app, mock_data):
    with TestClient(mock_app) as client:
        response = client.post('/users/', json=mock_data)
        assert response.status_code == 200
        data_stored = response.json()

        get_response = client.get('/users/')
        assert get_response.json()['user'] == [data_stored] 

def test_put(mock_app, mock_database, modified_data):
    with TestClient(mock_app) as client:
        modified_id = mock_database[0]['id']

        response = client.put(f"/users/{modified_id}", json=modified_data)

        assert response.status_code == 200
        mock_database[0]['name'] = modified_data['name']
        mock_database[0]['email'] = modified_data['email']

        get_response = client.get('/users/')

        assert mock_database == get_response.json()['user']

def test_delete(mock_app,mock_database):
    with TestClient(mock_app) as client:
        modified_id = mock_database[0]['id']

        response = client.delete(f'/users/{modified_id}')
        assert response.status_code == 200
        deleted_database = mock_database[1:]

        get_response = client.get('/users/')

        assert deleted_database == get_response.json()['user']