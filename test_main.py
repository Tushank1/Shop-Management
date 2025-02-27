import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

vendor_data = {
    "name": "Akash",
    "email": "ak@gmail.com",
    "password": "1234"
}

shop_data = [
    {
        "name": "Shop A",
        "type": "Electronics",
        "latitude": 40.712776,
        "longitude": -74.005974
    },
    {
        "name": "Shop B",
        "type": "Clothing",
        "latitude": 34.052235,
        "longitude": -118.243683
    },
    {
        "name": "Shop C",
        "type": "Grocery",
        "latitude": 51.507351,
        "longitude": -0.127758
    }
]

access_token = None

def test_register_vendor():
    response = client.post("/vendors/register",json=vendor_data)
    assert response.status_code==200 or response.status_code == 400
    
def test_login_vendor():
    global access_token
    response = client.get(f"/vendors/token?email={vendor_data['email']}&password={vendor_data['password']}")
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    assert access_token is not None

def test_create_shop():
    headers = {"Authorization": f"Bearer {access_token}"}
    for shop in shop_data:
        response = client.post("/shops/create",json=shop,headers=headers)
        assert response.status_code ==200
    
def test_get_shop():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/shops/retrieve",headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_shop():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/shops/retrieve", headers=headers)
    assert response.status_code == 200
    shop_list = response.json()
    assert len(shop_list) > 0
    
    shop_id = shop_list[0]["id"]
    update_data = {"name": "Updated Shop"}
    response = client.put(f"/shops/update/{shop_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Updated Shop"
    
def test_delete_shop():
    """Test Deleting a Shop"""
    headers = {"Authorization": f"Bearer {access_token}"}
    shop_id = 5
    response = client.delete(f"/shops/delete/{shop_id}", headers=headers)  # Assuming shop ID = 1
    assert response.status_code == 204

    
def test_public_api_nearby_shops():
    """Test Public API for Nearby Shops"""
    response = client.get("/search/nearby_shops?latitude=40.7128&longitude=-74.0060&radius=50")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    