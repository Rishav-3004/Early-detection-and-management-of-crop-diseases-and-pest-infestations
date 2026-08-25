import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # 1. Register
    reg_resp = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "New Farmer",
            "email": "newfarmer@agri.com",
            "password": "Password123!",
            "role": "FARMER"
        }
    )
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert reg_data["success"] is True
    assert "access_token" in reg_data["data"]

    # 2. Login
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "newfarmer@agri.com",
            "password": "Password123!"
        }
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["success"] is True
    assert login_data["data"]["email"] == "newfarmer@agri.com"

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, farmer_user):
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": farmer_user.email,
            "password": "WrongPassword!"
        }
    )
    assert resp.status_code == 401
    data = resp.json()
    assert data["success"] is False

@pytest.mark.asyncio
async def test_get_current_user_profile(client: AsyncClient, farmer_token: str, farmer_user):
    resp = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["id"] == farmer_user.id
