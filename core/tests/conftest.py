import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def use_test_db():
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    } 