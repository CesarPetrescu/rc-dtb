from fastapi.testclient import TestClient
from main import app
from db_init import init_db

init_db()
client = TestClient(app)

def test_login_and_create_user():
    # login with default admin user
    response = client.post('/auth/login', data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # create a new user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post('/users', params={"username": "test", "password": "test", "role": "CallCenter"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test"
    assert data["role"] == "CallCenter"
