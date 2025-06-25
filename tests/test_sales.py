from app.schemas.sales import SaleResponse

def test_get_sales(authorized_client, test_sales):
    response = authorized_client.get("api/v1/sales/")
    
    def validate(sale):
        return SaleResponse(**sale)
    
    sales = list(map(validate, response.json()))
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(sales) == len(test_sales)
    
    
def test_unauthorized_get_sales(client):
    response = client.get("api/v1/sales/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
    
def test_get_sale_by_id(authorized_client, test_sales):
    sale_id = test_sales[0].id
    response = authorized_client.get(f"api/v1/sales/{sale_id}")
    
    sale = SaleResponse(**response.json())
    
    assert response.status_code == 200
    assert sale.id == sale_id
    assert sale.item == test_sales[0].item
    assert sale.amount == test_sales[0].amount
    assert sale.quantity == test_sales[0].quantity
    
def test_sale_not_found(authorized_client):
    response = authorized_client.get("api/v1/sales/9999")
    
    assert response.status_code == 404
    
def test_unauthorized_get_sale_by_id(client, test_sales):
    sale_id = test_sales[0].id
    response = client.get(f"api/v1/sales/{sale_id}")
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
        
def test_create_sale(authorized_client, setup_user):
    sale_data = {
        "item": "Test Item",
        "amount": 100.0,
        "quantity": 2,
        "date": "2023-10-01",
        "owner_id": setup_user["id"]
    }
    response = authorized_client.post("api/v1/sales/", json=sale_data)
    assert response.status_code == 201
    new_sale = response.json()
    assert new_sale["item"] == sale_data["item"]
    assert new_sale["amount"] == sale_data["amount"]
    assert new_sale["quantity"] == sale_data["quantity"]
    assert new_sale["owner_id"] == setup_user["id"]
    
