import pytest
from api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """Shared API client for the whole test session."""
    return ApiClient()


@pytest.fixture
def new_booking_payload():
    """Reusable valid payload for booking-creation tests."""
    return {
        "firstname": "Jane",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-08-01",
            "checkout": "2026-08-05"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def created_booking_id(api_client, new_booking_payload):
    """Creates a booking and returns its id, for tests that need an
    existing record to read/update/delete against.
    """
    response = api_client.post("/booking", json=new_booking_payload)
    return response.json()["bookingid"]
