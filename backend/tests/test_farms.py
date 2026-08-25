import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_farm_and_field_lifecycle(client: AsyncClient, farmer_token: str):
    # 1. Create Farm
    create_farm_resp = await client.post(
        "/api/v1/farms",
        json={
            "name": "Sunny Hills Farm",
            "location": "Punjab",
            "area": 10.0,
            "soil_type": "Loam",
            "irrigation_type": "Drip"
        },
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert create_farm_resp.status_code == 201
    farm = create_farm_resp.json()["data"]
    farm_id = farm["id"]

    # 2. List Farms
    list_resp = await client.get(
        "/api/v1/farms",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert list_resp.status_code == 200
    farms = list_resp.json()["data"]
    assert any(f["id"] == farm_id for f in farms)

    # 3. Create Field
    create_field_resp = await client.post(
        "/api/v1/fields",
        json={
            "farm_id": farm_id,
            "name": "Tomato Sector 1",
            "area": 2.5,
            "variety": "Roma",
            "growth_stage": "Vegetative"
        },
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert create_field_resp.status_code == 201
    field = create_field_resp.json()["data"]
    assert field["farm_id"] == farm_id

    # 4. Get Field
    get_field_resp = await client.get(
        f"/api/v1/fields/{field['id']}",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert get_field_resp.status_code == 200
    assert get_field_resp.json()["data"]["name"] == "Tomato Sector 1"
