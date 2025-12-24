from src import app as app_module
import copy
import pytest

@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


def test_get_activities():
    data = app_module.get_activities()
    assert "Basketball Team" in data


def test_signup_and_refresh():
    email = "tester@example.com"
    activity = "Basketball Team"
    res = app_module.signup_for_activity(activity, email)
    assert "Signed up" in res["message"]
    assert email in app_module.activities[activity]["participants"]


def test_signup_already_exists():
    email = "james@mergington.edu"
    activity = "Basketball Team"
    with pytest.raises(app_module.HTTPException) as exc:
        app_module.signup_for_activity(activity, email)
    assert exc.value.status_code == 400


def test_unregister_participant():
    email = "unreg@example.com"
    activity = "Basketball Team"
    app_module.signup_for_activity(activity, email)
    res = app_module.unregister_participant(activity, email)
    assert "Unregistered" in res["message"]
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_not_found():
    email = "notregistered@example.com"
    activity = "Basketball Team"
    with pytest.raises(app_module.HTTPException) as exc:
        app_module.unregister_participant(activity, email)
    assert exc.value.status_code == 404
