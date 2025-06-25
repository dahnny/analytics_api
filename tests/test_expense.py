from app.schemas.expense import ExpenseResponse

def test_get_expense(authorized_client, test_expenses):
    response = authorized_client.get("api/v1/expenses/")
    
    def validate(expense):
        return ExpenseResponse(**expense)
    
    expenses = list(map(validate, response.json()))
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(expenses) == len(test_expenses)
    
def test_unauthorized_get_expense(client):
    response = client.get("api/v1/expenses/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
def test_get_expense_by_id(authorized_client, test_expenses):
    expense_id = test_expenses[0].id
    response = authorized_client.get(f"api/v1/expenses/{expense_id}")
    
    expense = ExpenseResponse(**response.json())
    
    assert response.status_code == 200
    assert expense.id == expense_id
    assert expense.item == test_expenses[0].item
    assert expense.amount == test_expenses[0].amount

def test_expense_not_found(authorized_client):
    response = authorized_client.get("api/v1/expenses/9999")
    
    assert response.status_code == 404
    
def test_unauthorized_get_expense_by_id(client, test_expenses):
    expense_id = test_expenses[0].id
    response = client.get(f"api/v1/expenses/{expense_id}")
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    
def test_create_expense(authorized_client, setup_user):
    expense_data = {
        "item": "Test Expense",
        "amount": 50.0,
        "category": "Office Supplies",
        "date": "2023-10-01",
        "owner_id": setup_user["id"]
    }
    response = authorized_client.post("api/v1/expenses/", json=expense_data)
    assert response.status_code == 201
    new_expense = response.json()
    assert new_expense["item"] == expense_data["item"]
    assert new_expense["amount"] == expense_data["amount"]
    assert new_expense["owner_id"] == setup_user["id"]
    
def test_update_expense(authorized_client, test_expenses):
    expense_id = test_expenses[0].id
    update_data = {
        "item": "Updated Expense",
        "amount": 75.0,
        "category": "Utilities",
        "date": "2023-10-02"
    }
    response = authorized_client.put(f"api/v1/expenses/{expense_id}", json=update_data)
    
    assert response.status_code == 200
    updated_expense = ExpenseResponse(**response.json())
    assert updated_expense.id == expense_id
    assert updated_expense.item == update_data["item"]
    assert updated_expense.amount == update_data["amount"]
    assert updated_expense.category == update_data["category"]