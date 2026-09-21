from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original_activities = deepcopy(activities)
    client = TestClient(app)
    yield client
    activities.clear()
    activities.update(deepcopy(original_activities))


def test_signup_adds_participant_without_refresh(client):
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


def test_unregister_participant_removes_email(client):
    activity_name = "Track and Field"
    email = "student@mergington.edu"

    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
