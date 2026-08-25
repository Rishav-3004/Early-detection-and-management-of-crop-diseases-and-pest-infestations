import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_expert_review_submission(
    client: AsyncClient,
    farmer_token: str,
    expert_token: str,
    sample_leaf_image_bytes: bytes
):
    # 1. Farmer scans
    files = {"file": ("leaf.jpg", sample_leaf_image_bytes, "image/jpeg")}
    scan_resp = await client.post(
        "/api/v1/detections/scan",
        files=files,
        headers={"Authorization": f"Bearer {farmer_token}"}
    )
    det_id = scan_resp.json()["data"]["id"]

    # 2. Expert lists pending cases
    pending_resp = await client.get(
        "/api/v1/experts/cases/pending",
        headers={"Authorization": f"Bearer {expert_token}"}
    )
    assert pending_resp.status_code == 200
    cases = pending_resp.json()["data"]
    assert any(c["id"] == det_id for c in cases)

    # 3. Expert submits review
    review_resp = await client.post(
        "/api/v1/experts/review",
        json={
            "detection_id": det_id,
            "verified_label": "Tomato Early Blight (Verified)",
            "corrected_confidence": 0.94,
            "severity": "MODERATE",
            "is_correct_prediction": True,
            "notes": "Visual confirmation of target board spots.",
            "recommendation": "Prune lower leaves and apply copper spray."
        },
        headers={"Authorization": f"Bearer {expert_token}"}
    )
    assert review_resp.status_code == 201
    assert review_resp.json()["data"]["verified_label"] == "Tomato Early Blight (Verified)"

@pytest.mark.asyncio
async def test_admin_analytics(client: AsyncClient, admin_token: str):
    resp = await client.get(
        "/api/v1/admin/analytics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "kpis" in data
    assert "model_metrics" in data
