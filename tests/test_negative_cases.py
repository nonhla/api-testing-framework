import pytest


class TestNegativeCases:
    """Error-handling coverage. Good API testing spends as much time here
    as on the happy path — this is usually where real bugs hide.
    """

    def test_get_nonexistent_user_returns_404(self, api_client):
        response = api_client.get("/users/9999")
        assert response.status_code == 404

    def test_get_users_invalid_page_type_does_not_500(self, api_client):
        # Malformed query params should never crash the server.
        response = api_client.get("/users?page=not_a_number")
        assert response.status_code != 500

    @pytest.mark.parametrize("bad_payload", [
        {},                          # empty payload
        {"name": ""},                # empty required field
        {"job": 12345},              # wrong type for field
    ])
    def test_create_user_with_invalid_payload_is_handled_gracefully(self, api_client, bad_payload):
        response = api_client.post("/users", json=bad_payload)
        # This API is lenient, but the assertion documents the expected
        # contract: never a raw 500, always a defined response.
        assert response.status_code < 500
