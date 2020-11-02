import os
import sys
import uuid

import pytest
from django.test import Client
from django.contrib.auth.models import User


sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def test_password():
    return 'strong-test-pass'

@pytest.fixture
def test_email():
    return 'test@mail.com'


@pytest.fixture
def create_user(db, django_user_model, test_password, test_email):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs['email'] = test_email
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user