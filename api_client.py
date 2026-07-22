"""Thin wrapper around requests for the API under test.

Keeping HTTP calls here (rather than inline in tests) means tests read like
specs, and if the API's base URL or auth scheme changes, there's one place
to update.
"""
import requests
from config import BASE_URL, DEFAULT_TIMEOUT, AUTH_USERNAME, AUTH_PASSWORD


class ApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self._token = None

    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", timeout=DEFAULT_TIMEOUT, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT, **kwargs)

    def authenticate(self) -> str:
        """Restful-Booker requires a token (via POST /auth) for PUT/PATCH/DELETE.
        Cached per client instance so tests don't re-authenticate every call.
        """
        if self._token is None:
            response = self.post("/auth", json={"username": AUTH_USERNAME, "password": AUTH_PASSWORD})
            response.raise_for_status()
            self._token = response.json()["token"]
        return self._token

    def _auth_cookie(self):
        return {"token": self.authenticate()}

    def put(self, path: str, json=None, **kwargs):
        return self.session.put(
            f"{self.base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT,
            cookies=self._auth_cookie(), **kwargs
        )

    def patch(self, path: str, json=None, **kwargs):
        return self.session.patch(
            f"{self.base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT,
            cookies=self._auth_cookie(), **kwargs
        )

    def delete(self, path: str, **kwargs):
        return self.session.delete(
            f"{self.base_url}{path}", timeout=DEFAULT_TIMEOUT,
            cookies=self._auth_cookie(), **kwargs
        )
