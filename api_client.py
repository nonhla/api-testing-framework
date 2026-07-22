"""Thin wrapper around requests for the API under test.

Keeping HTTP calls here (rather than inline in tests) means tests read like
specs, and if the API's base URL or auth scheme changes, there's one place
to update.
"""
import requests
from config import BASE_URL, DEFAULT_TIMEOUT


class ApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", timeout=DEFAULT_TIMEOUT, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT, **kwargs)

    def put(self, path: str, json=None, **kwargs):
        return self.session.put(f"{self.base_url}{path}", json=json, timeout=DEFAULT_TIMEOUT, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", timeout=DEFAULT_TIMEOUT, **kwargs)
