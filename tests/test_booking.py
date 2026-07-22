import pytest


class TestBookingEndpoint:
    """Positive-path CRUD coverage for the /booking endpoint."""

    def test_ping_confirms_api_is_up(self, api_client):
        response = api_client.get("/ping")
        assert response.status_code in (200, 201)

    def test_get_booking_ids_returns_list(self, api_client):
        response = api_client.get("/booking")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0
        assert "bookingid" in body[0]

    def test_create_booking_returns_id_and_echoes_payload(self, api_client, new_booking_payload):
        response = api_client.post("/booking", json=new_booking_payload)
        assert response.status_code == 200
        body = response.json()
        assert "bookingid" in body
        assert body["booking"]["firstname"] == new_booking_payload["firstname"]
        assert body["booking"]["lastname"] == new_booking_payload["lastname"]

    def test_get_single_booking_returns_expected_fields(self, api_client, created_booking_id):
        response = api_client.get(f"/booking/{created_booking_id}")
        assert response.status_code == 200
        booking = response.json()
        assert set(["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"]).issubset(booking.keys())

    def test_update_booking_returns_200(self, api_client, created_booking_id, new_booking_payload):
        updated_payload = {**new_booking_payload, "lastname": "Smith"}
        response = api_client.put(f"/booking/{created_booking_id}", json=updated_payload)
        assert response.status_code == 200
        assert response.json()["lastname"] == "Smith"

    def test_partial_update_booking_returns_200(self, api_client, created_booking_id):
        response = api_client.patch(f"/booking/{created_booking_id}", json={"firstname": "Janet"})
        assert response.status_code == 200
        assert response.json()["firstname"] == "Janet"

    def test_delete_booking_returns_201(self, api_client, created_booking_id):
        # Restful-Booker's documented (if unusual) success code for DELETE is 201.
        response = api_client.delete(f"/booking/{created_booking_id}")
        assert response.status_code == 201
