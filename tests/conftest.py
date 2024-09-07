import pytest

from tests import seed_database
from app import app


@pytest.fixture(scope="module")
def seed():
    """Seed database for tests"""
    seed_database()


@pytest.fixture(scope="module")
def client(seed):
    """Get test client from Flask"""
    return app.test_client()
