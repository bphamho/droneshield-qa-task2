"""Test cases to test store functionality"""
import pytest
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "https://petstore.swagger.io/v2"

@pytest.fixture(name="order_data")
def sample_order_data():
    """Sample order data"""
    return {
        "id": 2,
        "petId": 12345,
        "quantity": 2,
        "shipDate": "2024-11-13T12:15:45.209Z",
        "status": "placed",
        "complete": True
    }

@pytest.fixture(name="pet_data")
def sample_pet_data():
    """Sample pet data"""
    return {
        "id": 12345,
        "category": {"id": 0, "name": "dog"},
        "name": "Oreo2",
        "photoUrls":
            ["https://images.pexels.com/photos/23542021/pexels-photo-23542021/free-photo-of-brown-pomeranian-dog.jpeg"],
        "tags": [{"id": 0, "name": "tag1"}],
        "status": "test123"
    }

def test_place_get_order(pet_data, order_data):
    """Test placing and getting an order"""
    
    # First create a pet
    response = requests.post(f"{URL}/pet", json=pet_data)
    assert response.status_code == 200
    
    # Place an order for the created pet
    response = requests.post(f"{URL}/store/order", json=order_data)
    assert response.status_code == 200
    
    # Get order
    response = requests.get(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 200

def test_get_inventory(pet_data, order_data):
    """Test getting pet inventory"""
    
    # Create a pet
    response = requests.post(f"{URL}/pet", json=pet_data)
    assert response.status_code == 200
    
    # Verify they are in the inventory
    response = requests.get(f"{URL}/store/inventory")
    
    print(response.json())
    assert response.status_code == 200
    assert response.json()["test123"] == 1
    

def test_delete_order(order_data):
    """Test deleting an order"""
    
    # First verify order exists
    response = requests.get(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 200
    
    # Now delete order
    response = requests.delete(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 200
    
    # Check order doesnt exist
    response = requests.get(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 404

def test_get_nonexistent_order():
    """Test getting an invalid order"""
    
    # Get invalid order
    response = requests.get(f"{URL}/store/order/99999996", timeout=10)
    assert response.status_code == 404

def test_invalid_quantity(order_data):
    """Test placing an order with no quantity"""
    new_order = order_data.copy()
    del new_order["quantity"]
    
    response = requests.post(f"{URL}/store/order", json=new_order)
    assert response.status_code != 200

def test_negative_quantity(order_data):
    """Test placing an order with negative quantity"""
    new_order = order_data.copy()
    new_order["quantity"] = -20
    
    response = requests.post(f"{URL}/store/order", json=new_order)
    assert response.status_code != 200

def test_large_quantity(order_data):
    """Test placing an order with a large quantity"""
    new_order = order_data.copy()
    new_order["quantity"] = 1000000
    
    response = requests.post(f"{URL}/store/order", json=new_order)
    assert response.status_code != 200

def test_delete_twice(order_data):
    """Test attempting to delete an order twice"""
    
    # Create order
    response = requests.post(f"{URL}/store/order", json=order_data)
    assert response.status_code == 200
    
    # Now delete order
    response = requests.delete(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 200
    
    # Check order doesnt exist
    response = requests.get(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 404
    
    # Attempt to delete again
    response = requests.delete(f"{URL}/store/order/{order_data["id"]}", timeout=10)
    assert response.status_code == 404

def place_order_concurrently(test_order_data, num_requests=10):
    """Function to place orders concurrently"""
    
    def place_order():
        response = requests.post(f"{URL}/store/order", json=test_order_data) 
        assert response.status_code == 200
    
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(place_order) for _ in range(num_requests)]
        for future in futures:
            future.result()

def test_concurrent_orders(order_data):
    """Test placing concurrent orders"""
    
    place_order_concurrently(order_data, num_requests=20)

def test_high_volume_requests(order_data):
    """Test handling of high volume requests to ensure API performance under load"""
    num_requests = 100
    # Place order
    response = requests.post(f"{URL}/store/order", json=order_data)
    assert response.status_code == 200

    # Helper function to get pet data
    def place_order():
        response = requests.get(f"{URL}/store/order/{order_data["id"]}")
        assert response.status_code == 200

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(place_order) for _ in range(num_requests)]
        for future in futures:
            future.result()
