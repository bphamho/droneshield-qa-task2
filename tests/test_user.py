"""Test cases to test user functionality"""
import pytest
import requests

URL = "https://petstore.swagger.io/v2"

@pytest.fixture(name="user_data")
def sample_user_data():
    """Sample user data"""
    return {
        "id": 123,
        "username": "Test",
        "firstName": "First",
        "lastName": "Last",
        "email": "first_last@test.com",
        "password": "root",
        "phone": 987654321,
        "userStatus": 0
    }

def test_create_user(user_data):
    """Test to create new user"""
    response = requests.post(f"{URL}/user", json=user_data)
    assert response.status_code == 200
    
    # Check user is created
    assert response.json()["message"] == str(user_data["id"])

def test_login(user_data):
    """Test login with new user"""
    response = requests.get(f"{URL}/user/login", params={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200

def test_logout():
    """Test logout with user"""
    response = requests.get(f"{URL}/user/logout")
    assert response.status_code == 200

def test_update_user(user_data):
    """Test updating a user"""