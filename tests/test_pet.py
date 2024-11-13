"""Test cases to test pet functionality"""
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "https://petstore.swagger.io/v2"

@pytest.fixture(name="pet_data")
def sample_pet_data():
    """Sample pet data"""
    return {
        "id": 12345,
        "category": {"id": 0, "name": "dog"},
        "name": "Oreo",
        "photoUrls":
            ["https://images.pexels.com/photos/23542021/pexels-photo-23542021/free-photo-of-brown-pomeranian-dog.jpeg"],
        "tags": [{"id": 0, "name": "tag1"}],
        "status": "available"
    }

# Basic Functionality
def test_create_pet(pet_data):
    """Test creating pet data from sample"""
    response = requests.post(f"{URL}/pet", json=pet_data, timeout=10)
    assert response.status_code == 200
    assert response.json()["name"] == pet_data["name"]
    print("Succesfully created pet data")

def test_get_petid(pet_data):
    """Test getting pet id"""
    pet_id = pet_data["id"]

    # Verify pet is created
    requests.post(f"{URL}/pet", json=pet_data, timeout=10)

    response = requests.get(f"{URL}/pet/{pet_id}", timeout=10)

    # Check pet id
    assert response.status_code == 200
    assert response.json()["id"] == pet_id

def test_update_pet(pet_data):
    """Test updating pet information"""
    # Create new pet
    requests.post(f"{URL}/pet", json=pet_data, timeout=10)
    updated_data = pet_data.copy()
    updated_data["name"] = "Bolt"

    # Update pet with new pet
    response = requests.put(f"{URL}/pet", json=updated_data, timeout=10)
    assert response.status_code == 200
    assert response.json()["name"] == "Bolt"

def test_delete_pet(pet_data):
    """Test deleting pet"""
    pet_id = pet_data["id"]
    # Create pet
    requests.post(f"{URL}/pet", json=pet_data, timeout=10)

    response = requests.delete(f"{URL}/pet/{pet_id}", timeout=10)
    assert response.status_code == 200

    # Verify pet doesn't exist
    response = requests.get(f"{URL}/pet/{pet_id}", timeout=10)
    assert response.status_code == 404

def test_find_pets_by_status(pet_data):
    """Test to find pets by different status's"""
    # First create pets with different statuses (available, pending, sold)
    pet_pending = pet_data.copy()
    pet_pending["id"] = 71
    pet_pending["status"] = "pending"
    
    pet_sold = pet_data.copy()
    pet_sold["id"] = 72
    pet_sold["status"] = "sold"
    
    response = requests.post(f"{URL}/pet", json=pet_pending, timeout=10)
    assert response.status_code == 200

    response = requests.post(f"{URL}/pet", json=pet_sold, timeout=10)
    assert response.status_code == 200

    # Test for 'available' status
    response = requests.get(f"{URL}/pet/findByStatus", params={"status": "available"})
    assert response.status_code == 200
    for pet in response.json():
        assert pet["status"] == "available"

    # Test for 'pending' status
    response = requests.get(f"{URL}/pet/findByStatus", params={"status": "pending"})
    assert response.status_code == 200
    for pet in response.json():
        assert pet["status"] == "pending"

    # Test for 'sold' status
    response = requests.get(f"{URL}/pet/findByStatus", params={"status": "sold"})
    assert response.status_code == 200
    for pet in response.json():
        assert pet["status"] == "sold"

    # Test for empty field
    response = requests.get(f"{URL}/pet/findByStatus", params={"status": ""})
    assert response.status_code == 200

    # Test for no status parameter
    response = requests.get(f"{URL}/pet/findByStatus")
    assert response.status_code == 200

def test_special_characters(pet_data):
    """Test creating a pet with special characters (symbols and unicode)"""
    special_names = [
        "!@#$%^",
        "Oreo\n",
        "Luna\t",
        "<script>alert('test')</script>",  # Injection
        "🤓", # Unicode emoji
    ]
    
    for name in special_names:
        new_pet = pet_data.copy()
        new_pet["name"] = name
        response = requests.post(f"{URL}/pet", json=new_pet, timeout=10)

        assert response.status_code in {200, 201}

def test_update_pet_form(pet_data):
    """Test updating a pet with form data"""
    
    # Create pet
    new_pet = pet_data.copy()
    new_pet["id"] = 678
    
    new_data = {
        "name" : "NewName",
        "status": "sold"
    }
    response = requests.post(f"{URL}/pet", json=new_pet)
    assert response.status_code == 200
    
    # Update pet with form data
    response = requests.post(f"{URL}/pet/{new_pet["id"]}", data=new_data)
    assert response.status_code == 200
    
    # Verify pet new data
    response = requests.get(f"{URL}/pet/{new_pet["id"]}", timeout=10)
    assert response.status_code == 200
    assert response.json()["name"] == new_data["name"]
    assert response.json()["status"] == new_data["status"]

def test_flow():
    """Test a start to finish creation, get, update, get and deletion of a pet"""
    
    # Create pet
    test_pet_data ={
        "id": 54321,
        "name": "Bolt",
        "category": {"id": 1, "name": "Dogs"},
        "status": "available"
    }
    
    response = requests.post(f"{URL}/pet", json=test_pet_data)
    assert response.status_code == 200
    
    # Get pet details to confirm creation
    response = requests.get(f"{URL}/pet/{test_pet_data['id']}", timeout=10)
    assert response.json()["name"] == "Bolt"
    
    # Update pet details
    new_pet = test_pet_data.copy()
    new_pet["status"] = "sold"
    new_pet["name"] = "Bolt2"
    response = requests.post(f"{URL}/pet", json=new_pet)
    assert response.status_code == 200
    
    # Get pet name and status to confirm update
    response = requests.get(f"{URL}/pet/{test_pet_data['id']}", timeout=10)
    assert response.json()["name"] == "Bolt2"
    assert response.json()["status"] == "sold"
    
    # Delete pet
    response = requests.delete(f"{URL}/pet/{test_pet_data['id']}")
    assert response.status_code == 200
    
    # Confirm pet has been delete
    response = requests.get(f"{URL}/pet/{test_pet_data['id']}", timeout=10)
    assert response.status_code == 404

def test_invalid_name(pet_data):
    """Test passing invalid name to API"""
    new_pet = pet_data.copy()
    new_pet.pop("name", None)
    response = requests.post(f"{URL}/pet", json=pet_data, timeout=10)
    # Verify if not accepted
    assert response.status_code != 200

def test_large_id(pet_data):
    """Test passing a large id"""
    new_pet = pet_data.copy()

    # id is in int64, maximum value for int64 is 2^(63-1)
    new_pet["id"] = 2**(63)
    response = requests.post(f"{URL}/pet", json=new_pet, timeout=10)
    assert response.status_code == 500

def test_incorrect_json():
    """Test creating a pet with incorrect JSON data"""
    response = requests.post(f"{URL}/pet", data="{name: 'Buddy'}", timeout=10)
    assert response.status_code == 415

def test_null_pet():
    """Test attempting to get/delete a non existent pet"""
    
    # Try to get pet with id 99999999
    response = requests.get(f"{URL}/pet/99999999")
    assert response.status_code == 404
    
    # Try to delete pet
    response = requests.delete(f"{URL}/pet/99999999")
    assert response.status_code == 404

def test_negative_id():
    """Test passing in a negative pet id"""
    negative_id = -10
    response = requests.get(f"{URL}/pet{negative_id}", timeout=10)
    assert response.status_code == 404

def test_zero_id():
    """Test passing in pet id of 0"""
    zero_id = 0
    response = requests.get(f"{URL}/pet{zero_id}", timeout=10)
    assert response.status_code == 404

def test_missing_id(pet_data):
    """Test creating a pet with no id"""
    new_pet = pet_data.copy()
    new_pet.pop("id", None)
    
    response = requests.post(f"{URL}/pet", json=new_pet, timeout=10)
    
    assert response.status_code != 200

def test_invalid_http_method():
    """Test using an invalid HTTP method for an endpoint."""
    response = requests.put(f"{URL}/pet/findByStatus")

    # Expecting 405 Method Not Allowed
    assert response.status_code == 405

def create_pet_concurrently(test_pet_data, num_requests=10):
    """Function to create pets concurrently to check for race conditions or resource conflicts."""
    
    def create_pet():
        response = requests.post(f"{URL}/pet", json=test_pet_data)
        assert response.status_code == 200

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(create_pet) for _ in range(num_requests)]
        for future in futures:
            future.result()

def test_concurrent_pet_creation():
    """Test creating pets concurrently to check for race conditions or resource conflicts"""
    test_pet_data = {
        "id": 1234567,
        "name": "TestPet",
        "category": {"id": 1, "name": "Dogs"},
        "status": "available"
    }

    create_pet_concurrently(test_pet_data, num_requests=20)

def test_high_volume_requests():
    """Test handling of high volume requests to ensure API performance under load"""
    num_requests = 100
    
    # Helper function to get pet data
    def get_pet():
        response = requests.get(f"{URL}/pet/findByStatus", params={"status": "available"})
        assert response.status_code == 200

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_pet) for _ in range(num_requests)]
        for future in futures:
            future.result()
