"""Simulates persistence across session boundaries (AC-003 style)."""


def test_request_visible_in_new_session(client, sample_request_payload, db_session):
    created = client.post("/api/v1/requests", json=sample_request_payload)
    assert created.status_code == 201
    request_id = created.json()["id"]

    # Expire ORM identity map to force reload from DB
    db_session.expire_all()
    fetched = client.get(f"/api/v1/requests/{request_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == request_id
