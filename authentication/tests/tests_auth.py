import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('user','user@mail.com','user_pass')
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_home_view(client):
    url = '/login/?=next/'
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_home_view_with_logged_user(client, create_user, test_password):
    user = create_user(username='user')
    url = '/'
    client.login(
        username=user.username, password=test_password
    )
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_reset_password(client):
    url = reverse('auth:password_reset')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_reset_password_send(client, create_user, test_email, mailoutbox):
    user = create_user(username='user')
    url = reverse('auth:password_reset')
    response = client.post(url, {'email': test_email})
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    response = client.get('password_reset/done/')
    assert response.status_code == 200