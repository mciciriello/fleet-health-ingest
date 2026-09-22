from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ingest_rejects_incomplete_payload() -> None:
    response = client.post("/ingest", json={"host": "navi-01"})
    assert response.status_code == 422


def test_ingest_rejects_cpu_out_of_range() -> None:
    response = client.post(
        "/ingest",
        json={"host": "navi-01", "cpu_pct": 140, "mem_pct": 10, "ok": True},
    )
    assert response.status_code == 422


def test_latest_rejects_bad_limit() -> None:
    response = client.get("/latest", params={"limit": 0})
    assert response.status_code == 400
