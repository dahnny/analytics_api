from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.core.config import settings
from app.api.deps import get_db
from app.models.base import Base
from app.models.sales import Sale
from app.schemas.user import UserResponse
from app.models.expense import Expense
from app.core.token import create_access_token
import pytest

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=f'{settings.database_names}_test'
)
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


        
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture()       
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
        

@pytest.fixture
def setup_user(client):
    user_data = {
        "email": "danielogbuti@gmail.com",
        "password": "password123"
        }
    response = client.post("api/v1/users/", json=user_data)
    
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(setup_user):
   return create_access_token(data={"user_id": setup_user["id"]})  

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_sales(session, setup_user):
    sales_data = [
        {
            "item": "Item 1",
            "amount": 50.0,
            "quantity": 1,
            "date": "2023-10-01",
            "owner_id": setup_user["id"]
        },
        {
            "item": "Item 2",
            "amount": 150.0,
            "quantity": 3,
            "date": "2023-10-02",
            "owner_id": setup_user["id"]
        }
    ]
    def create_sale_model(sale):
        return Sale(**sale)
    
    sale = list(map(create_sale_model, sales_data))
    session.add_all(sale)
    session.commit()
    return(session.query(Sale).all())
    
@pytest.fixture    
def test_expenses(session, setup_user):
    expenses_data = [
        {
            "item": "Expense 1",
            "amount": 30.0,
            "category": "Utilities",
            "date": "2023-10-01",
            "owner_id": setup_user["id"]
        },
        {
            "item": "Expense 2",
            "amount": 80.0,
            "category": "Office Supplies",
            "date": "2023-10-02",
            "owner_id": setup_user["id"]
        }
    ]
    
    def create_expense_model(expense):
        return Expense(**expense)
    
    expense = list(map(create_expense_model, expenses_data))
    session.add_all(expense)
    session.commit()
    return(session.query(Expense).all())
    
    