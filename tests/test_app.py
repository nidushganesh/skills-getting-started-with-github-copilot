from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_adds_participant_without_refresh():
    activity_name = "Soccer Club"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
