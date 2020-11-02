import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_403_handler(auto_login_user):
    url = '/download_data/'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_404_handler(client):
    url = '/not_existing_page/'
    response = client.get(url)
    print(response)
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_exist(auto_login_user):
    url = '/team/20'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_not_exist(auto_login_user):
    url = '/team/21'
    client, user = auto_login_user()
    try:
        response = client.get(url)
    except:
        response = None
    assert response == None

@pytest.mark.django_db
def test_player_exist(auto_login_user):
    url = '/player/200'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_player_not_exist(auto_login_user):
    url = '/player/999999'
    client, user = auto_login_user()
    try:
        response = client.get(url)
    except:
        response = None
    assert response == None

@pytest.mark.django_db
def test_fixtures(auto_login_user):
    url = '/fixtures/'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_standings(auto_login_user):
    url = '/standings/'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_stats(auto_login_user):
    url = '/stats/'
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200
