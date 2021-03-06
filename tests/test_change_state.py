from flask import json


def test_activate_inactive(client, auth_token, sample_project, project_dao):
    """Activating an inactive project sets active to True, returns 204"""
    # Given
    project_id = sample_project["uid"];
    project_dao.update(project_id, {"active": False})

    # When
    response = client.post("/projects/%s" % project_id,
                           data={'active': True},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    update_project = project_dao.get(project_id)
    assert update_project['active'] is True
    assert 200 == response.status_code


def test_deactivating_active(client, auth_token, sample_project):
    """Deactivating an active projects sets active to False, returns 204"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={'active': False},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    saved_project = json.loads(client.get("/projects/%s" % project_id).data)
    assert saved_project['active'] is False
    assert 200 == response.status_code


def test_deactivate_not_existing_project(client, auth_token, sample_project):
    """Deactivating a not existing project returns 404"""
    # Given
    assert sample_project
    # When
    response = client.post("/projects/%s" % 789,
                           data={'active': True},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 404 == response.status_code


def test_activate_not_existing(client, auth_token):
    """Activating a not existing project returns 404"""
    # When
    response = client.post("/projects/%s" % 789,
                           data={'active': False},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 404 == response.status_code


def test_empty_request(client, auth_token, sample_project):
    """Given an empty request it should return 400"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 400 == response.status_code


def test_invalid_request(client, auth_token, sample_project):
    """Given an invalid request it should return 400"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={"invalid_field": "value"},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 400 == response.status_code
