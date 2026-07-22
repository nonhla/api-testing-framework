import pytest
from api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """Shared API client for the whole test session."""
    return ApiClient()


@pytest.fixture
def new_user_payload():
    """Reusable valid payload for user-creation tests."""
    return {"name": "Jane Doe", "job": "QA Engineer"}
