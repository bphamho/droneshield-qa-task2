"""Test cases to test user functionality"""
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "https://petstore.swagger.io/v2"

@pytest.fixture(name="user_data")
def sample_user_data():
    """Sample user data"""
    return {
        "id": 123,
        "username": "Test1234",
        "firstName": "First",
        "lastName": "Last",
        "email": "first_last@test.com",
        "password": "root",
        "phone": 987654321,
        "userStatus": 0
    }

def test_create_get_user(user_data):
    """Test to create and get new user"""
    response = requests.post(f"{URL}/user", json=user_data)
    assert response.status_code == 200
    
    # Check user is created
    assert response.json()["message"] == str(user_data["id"])
    
    response = requests.get(f"{URL}/user/{user_data["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["firstName"] == user_data["firstName"]

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
    update_user = user_data.copy()
    update_user["firstName"] = "First1st"
    update_user["lastName"] = "Lastst"
    update_user["email"] = "first1st_lastst@test.com"
    print(update_user)
    response = requests.put(f"{URL}/user/{user_data["username"]}", json=update_user)
    assert response.status_code == 200
    
    # Check if user has been updated
    response = requests.get(f"{URL}/user/{update_user["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["firstName"] == update_user["firstName"]
    assert response.json()["lastName"] == update_user["lastName"]
    assert response.json()["email"] == update_user["email"]

def test_delete_user(user_data):
    """Test deeting a user"""
    delete_user = user_data.copy()
    delete_user["username"] = "Test123456"
    
    # Create new user first
    response = requests.post(f"{URL}/user", json=delete_user)
    assert response.status_code == 200
    
    # Now delete user
    response = requests.delete(f"{URL}/user/{delete_user["username"]}")
    assert response.status_code == 200
    
    # Verify user has been deleted
    response = requests.get(f"{URL}/user/{delete_user["username"]}", timeout=10)
    assert response.status_code == 404

def test_create_list(user_data):
    """Test creating lists of users"""
    user1 = user_data.copy()
    user2 = user_data.copy()
    
    user1["username"] = "user1"
    user1["id"] = 124
    user2["username"] = "user2"
    user2["id"] = 125
    
    user_list = [user1, user2]
    
    # Create with list
    response = requests.post(f"{URL}/user/createWithList", json=user_list)
    
    assert response.status_code == 200
    
    # Verify 2 users were created
    response = requests.get(f"{URL}/user/{user1["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["username"] == "user1"

    response = requests.get(f"{URL}/user/{user2["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["username"] == "user2"

def test_create_array(user_data):
    """Test creating array of users"""
    user3 = user_data.copy()
    user4 = user_data.copy()
    
    user3["username"] = "user3"
    user3["id"] = 126
    user4["username"] = "user4"
    user4["id"] = 127
    
    user_array = [user3, user4]
    
    # Create with array
    response = requests.post(f"{URL}/user/createWithArray", json=user_array)
    
    assert response.status_code == 200
    # Verify 2 users were created
    response = requests.get(f"{URL}/user/{user3["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["username"] == "user3"

    response = requests.get(f"{URL}/user/{user4["username"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["username"] == "user4"

def test_incorrect_json():
    """Test creating a pet with incorrect JSON data"""
    response = requests.post(f"{URL}/user", data="{username: 'Test1234'}", timeout=10)
    assert response.status_code == 415

def test_get_none_user():
    """Test getting a None user"""
    response = requests.get(f"{URL}/user/{None}", timeout=10)
    assert response.status_code == 404

def test_create_none_user(user_data):
    """Test creating a None username"""
    none_user = user_data.copy()
    none_user["username"] = None
    
    response= requests.post(f"{URL}/user", json=none_user)
    assert response.status_code != 200

def test_get_nonexistent_user():
    """Test getting a non existent user"""
    response = requests.get(f"{URL}/user/99999999", timeout=10)
    assert response.status_code == 404

def test_long_username(user_data):
    """Test creating a user with a long username"""
    test_user = user_data.copy()
    test_user['username'] = "a" * 10000
    response= requests.post(f"{URL}/user", json=test_user)
    
    assert response.status_code == 200
    
    # Make sure username matches
    response= requests.get(f"{URL}/user/{test_user["username"]}", timeout=10)
    assert response.json()["username"] == test_user["username"]

def create_users_concurrently(test_user_data, num_requests=10):
    """Function to create users concurrently to check for race conditions or resource conflicts."""
    
    def create_pet():
        response = requests.post(f"{URL}/user", json=test_user_data)
        assert response.status_code == 200

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(create_pet) for _ in range(num_requests)]
        for future in futures:
            future.result()

def test_concurrent_user_creation(user_data):
    """Test concurrent creation of a user"""
    create_users_concurrently(user_data, num_requests=20)

def test_high_volume_requests(user_data):
    """Test handling of high volume requests to ensure API performance under load"""
    num_requests = 100
    
    # Helper function to get pet data
    def get_user():
        response = requests.get(f"{URL}/user/{user_data["username"]}")
        assert response.status_code == 200

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_user) for _ in range(num_requests)]
        for future in futures:
            future.result()