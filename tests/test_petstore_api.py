"""Test"""
import pytest
import requests

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

def test_invalid_name(pet_data):
    """Test passing invalid name to API"""
    new_pet = pet_data.copy()
    new_pet["name"] = None
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
