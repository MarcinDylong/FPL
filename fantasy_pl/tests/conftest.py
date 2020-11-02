import os
import sys
import uuid
import pytest
import psycopg2

from django.test import Client
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login

def run_sql(sql):
    conn = psycopg2.connect(database='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()

@pytest.fixture(scope='session')
def django_db_setup():
    pass

@pytest.fixture
def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)
