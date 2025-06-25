from app.schemas.user import UserResponse
from app.schemas.token import Token
from app.core.config import settings
from jose import jwt
import pytest


def test_create_user(client):
    response = client.post(
        "api/v1/users/",
        json={
            "email": "danielogbuti@gmail.com",
            "password": "password123"
        })
    new_user = UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "danielogbuti@gmail.com"
    
def test_login_user(setup_user, client):
    response = client.post(
        "api/v1/auth/login",
        data={
            "username": "danielogbuti@gmail.com",
            "password": "password123"
        })
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert response.status_code == 200
    assert id == setup_user["id"]
    assert login_res.token_type == "bearer"
    
    
def test_login_user_invalid_credentials(setup_user, client):
    response = client.post(
        "api/v1/auth/login",
        data={
            "username": setup_user["email"],
            "password": "wrongpassword"
            })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials",}
    
    

    
    