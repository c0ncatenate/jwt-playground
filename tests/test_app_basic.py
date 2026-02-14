from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_index_page_renders():
    response = client.get("/")
    assert response.status_code == 200
    assert "JWT Playground" in response.text


def test_normal_scenario_issue_token():
    response = client.post("/normal/issue", data={"username": "alice"})
    assert response.status_code == 200
    assert "Issued token" in response.text
    assert "alice" in response.text


def test_tamper_scenario_resign_and_forge():
    # Use a simple payload for both paths
    payload_json = '{"sub": "alice", "role": "user"}'

    # Resign path
    resign_resp = client.post(
        "/tamper/experiment",
        data={"payload_json": payload_json, "resign": "1"},
    )
    assert resign_resp.status_code == 200
    assert "Issued from tampered payload" in resign_resp.text

    # Forged path
    forged_resp = client.post(
        "/tamper/experiment",
        data={"payload_json": payload_json},
    )
    assert forged_resp.status_code == 200
    assert "Unsigned / forged token" in forged_resp.text


def test_expiry_scenario_valid_and_expired():
    # Valid token
    valid_resp = client.post(
        "/expiry/issue",
        data={
            "username": "alice",
            "lifetime_seconds": "60",
            "backdated_seconds": "0",
        },
    )
    assert valid_resp.status_code == 200
    assert "Issued token" in valid_resp.text
    assert "Status:" in valid_resp.text

    # Expired token: backdate beyond lifetime
    expired_resp = client.post(
        "/expiry/issue",
        data={
            "username": "alice",
            "lifetime_seconds": "10",
            "backdated_seconds": "20",
        },
    )
    assert expired_resp.status_code == 200
    assert "Token expired" in expired_resp.text


def test_bad_practices_scenario():
    weak_resp = client.post("/bad/issue-hs256", data={"username": "alice"})
    assert weak_resp.status_code == 200
    assert "Issued with weak secret" in weak_resp.text

    alg_none_resp = client.post(
        "/bad/accept-alg-none",
        data={"token": "header.payload.signature"},
    )
    assert alg_none_resp.status_code == 200
    assert "alg=none" in alg_none_resp.text
