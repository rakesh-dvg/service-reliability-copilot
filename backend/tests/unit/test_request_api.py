def test_create_and_list_request(client, sample_request_payload):
    created = client.post("/api/v1/requests", json=sample_request_payload)
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "Printer offline"
    assert body["status"] == "open"

    listed = client.get("/api/v1/requests")
    assert listed.status_code == 200
    assert any(item["id"] == body["id"] for item in listed.json())


def test_validation_rejects_bad_email(client, sample_request_payload):
    sample_request_payload["customer_email"] = "not-an-email"
    response = client.post("/api/v1/requests", json=sample_request_payload)
    assert response.status_code == 422


def test_demo_failure_returns_503(client, sample_request_payload, admin_headers):
    enable = client.post("/api/v1/demo/failure/enable", headers=admin_headers)
    assert enable.status_code == 200
    failed = client.post("/api/v1/requests", json=sample_request_payload)
    assert failed.status_code == 503

    disable = client.post("/api/v1/demo/failure/disable", headers=admin_headers)
    assert disable.status_code == 200
    ok = client.post("/api/v1/requests", json=sample_request_payload)
    assert ok.status_code == 201


def test_status_transition_requires_admin(client, sample_request_payload, admin_headers):
    created = client.post("/api/v1/requests", json=sample_request_payload).json()
    unauthorized = client.patch(
        f"/api/v1/requests/{created['id']}/status",
        json={"status": "in_progress"},
    )
    assert unauthorized.status_code == 401

    updated = client.patch(
        f"/api/v1/requests/{created['id']}/status",
        json={"status": "in_progress"},
        headers=admin_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "in_progress"


def test_invalid_status_transition(client, sample_request_payload, admin_headers):
    created = client.post("/api/v1/requests", json=sample_request_payload).json()
    response = client.patch(
        f"/api/v1/requests/{created['id']}/status",
        json={"status": "completed"},
        headers=admin_headers,
    )
    assert response.status_code == 400
