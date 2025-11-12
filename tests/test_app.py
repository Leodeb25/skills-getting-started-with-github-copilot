from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure email not present initially; if present, try to remove it
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    if email in participants:
        client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={email}")

    # Sign up
    r = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Verify presence
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    assert email in participants

    # Unregister
    r = client.post(f"/activities/{urllib.parse.quote(activity)}/unregister?email={email}")
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Verify removal
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    assert email not in participants


def test_signup_existing_returns_400():
    activity = "Chess Club"
    email = "michael@mergington.edu"  # exists in sample data
    r = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={email}")
    assert r.status_code == 400
