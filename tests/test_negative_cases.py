import pytest


class TestNegativeCases:
    """Error-handling and edge-case coverage. Good API testing spends as
    much time here as on the happy path — this is usually where real
    bugs hide.
    """

    def test_get_nonexistent_booking_returns_404(self, api_client):
        response = api_client.get("/booking/999999999")
        assert response.status_code == 404

    def test_update_booking_without_auth_is_rejected(self, api_client, created_booking_id, new_booking_payload):
        # Deliberately bypass the client's auto-auth to confirm the API
        # actually enforces it, rather than assuming it does.
        response = api_client.session.put(
            f"{api_client.base_url}/booking/{created_booking_id}",
            json=new_booking_payload,
        )
        assert response.status_code in (401, 403)

    def test_delete_booking_without_auth_is_rejected(self, api_client, created_booking_id):
        response = api_client.session.delete(f"{api_client.base_url}/booking/{created_booking_id}")
        assert response.status_code in (401, 403)

    @pytest.mark.xfail(
        reason="Known Restful-Booker bug: incomplete payloads return a raw "
                "500 instead of a 4xx client error. Tracked here rather than "
                "silently loosened so the regression stays visible.",
        strict=True,
    )
    @pytest.mark.parametrize("bad_payload", [
        {},                                    # empty payload
        {"firstname": "OnlyFirstName"},        # missing required fields
    ])
    def test_create_booking_with_incomplete_payload_is_handled_gracefully(self, api_client, bad_payload):
        """KNOWN BUG (found via this test): Restful-Booker returns a raw
        500 Internal Server Error for incomplete payloads instead of a
        4xx client error. Marked xfail(strict=True) so it shows clearly
        in test output as a documented, tracked defect rather than a
        silent pass or a build-breaking failure — and if the API is ever
        fixed, strict mode will flag this test so it can be re-enabled.
        """
        response = api_client.post("/booking", json=bad_payload)
        assert response.status_code < 500, (
            f"Expected a 4xx client error for incomplete payload, got "
            f"{response.status_code}."
        )

    def test_filter_bookings_by_name(self, api_client, new_booking_payload):
        # Create a booking with a distinctive name, then confirm the
        # name-filter query param actually narrows results.
        api_client.post("/booking", json=new_booking_payload)
        response = api_client.get(
            "/booking",
            params={"firstname": new_booking_payload["firstname"], "lastname": new_booking_payload["lastname"]},
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1
