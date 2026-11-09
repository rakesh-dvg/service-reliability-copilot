def test_incident_upsert_dedup_and_remediation(client, recovery_headers):
    first = client.post(
        "/api/v1/internal/incidents/upsert",
        headers=recovery_headers,
        json={
            "fingerprint": "fp-demo-1",
            "incident_type": "DEMO_FAILURE_MODE",
            "severity": "high",
            "root_cause": "demo failure enabled",
        },
    )
    assert first.status_code == 200
    assert first.json()["created"] is True
    incident_id = first.json()["id"]

    second = client.post(
        "/api/v1/internal/incidents/upsert",
        headers=recovery_headers,
        json={
            "fingerprint": "fp-demo-1",
            "incident_type": "DEMO_FAILURE_MODE",
            "severity": "high",
            "root_cause": "demo failure enabled",
        },
    )
    assert second.status_code == 200
    assert second.json()["created"] is False
    assert second.json()["id"] == incident_id

    rem = client.post(
        f"/api/v1/internal/incidents/{incident_id}/remediations",
        headers=recovery_headers,
        json={
            "action_type": "DISABLE_DEMO_FAILURE_MODE",
            "status": "succeeded",
            "diagnostic_summary": "disabled demo flag",
            "verification_result": "ok",
        },
    )
    assert rem.status_code == 200

    resolved = client.post(
        f"/api/v1/internal/incidents/{incident_id}/resolve",
        headers=recovery_headers,
        json={"recovery_verified": True},
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"
    assert resolved.json()["recovery_verified"] is True


def test_recovery_endpoint_disables_failure(
    client, admin_headers, recovery_headers, sample_request_payload
):
    client.post("/api/v1/demo/failure/enable", headers=admin_headers)
    assert client.post("/api/v1/requests", json=sample_request_payload).status_code == 503

    recovery = client.post(
        "/api/v1/internal/recovery/disable-demo-failure",
        headers=recovery_headers,
    )
    assert recovery.status_code == 200
    assert client.post("/api/v1/requests", json=sample_request_payload).status_code == 201


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "service_request_submissions_total" in response.text or response.text is not None
