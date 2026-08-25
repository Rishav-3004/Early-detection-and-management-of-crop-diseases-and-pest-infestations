import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_scan_crop_image_and_retrieve(
    client: AsyncClient,
    farmer_token: str,
    sample_leaf_image_bytes: bytes
):
    # 1. Upload scan
    files = {
        "file": ("leaf_test.jpg", sample_leaf_image_bytes, "image/jpeg")
    }
    scan_resp = await client.post(
        "/api/v1/detections/scan",
        files=files,
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert scan_resp.status_code == 201
    scan_data = scan_resp.json()
    assert scan_data["success"] is True
    det = scan_data["data"]
    assert "predicted_label" in det
    assert "confidence" in det
    assert "severity" in det
    assert "risk_score" in det
    assert "results" in det
    assert len(det["results"]) >= 1

    det_id = det["id"]

    # 2. Get Detection Detail
    detail_resp = await client.get(
        f"/api/v1/detections/{det_id}",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert detail_resp.status_code == 200
    detail_data = detail_resp.json()["data"]
    assert detail_data["id"] == det_id
    assert "recommendations" in detail_data

    # 3. List Detections
    list_resp = await client.get(
        "/api/v1/detections",
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    assert list_resp.status_code == 200
    list_data = list_resp.json()["data"]
    assert list_data["meta"]["total"] >= 1
