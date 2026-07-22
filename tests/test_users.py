import pytest


class TestUsersEndpoint:
    """Positive-path CRUD coverage for the /users endpoint."""

    @pytest.mark.parametrize("page", [1, 2])
    def test_get_users_list_returns_200(self, api_client, page):
        response = api_client.get(f"/users?page={page}")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert isinstance(body["data"], list)

    def test_get_single_user_returns_expected_fields(self, api_client):
        response = api_client.get("/users/2")
        assert response.status_code == 200
        user = response.json()["data"]
        assert set(["id", "email", "first_name", "last_name"]).issubset(user.keys())

    def test_create_user_returns_201_and_echoes_payload(self, api_client, new_user_payload):
        response = api_client.post("/users", json=new_user_payload)
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == new_user_payload["name"]
        assert body["job"] == new_user_payload["job"]
        assert "id" in body
        assert "createdAt" in body

    def test_update_user_returns_200(self, api_client, new_user_payload):
        updated_payload = {**new_user_payload, "job": "Senior QA Engineer"}
        response = api_client.put("/users/2", json=updated_payload)
        assert response.status_code == 200
        assert response.json()["job"] == "Senior QA Engineer"

    def test_delete_user_returns_204(self, api_client):
        response = api_client.delete("/users/2")
        assert response.status_code == 204
