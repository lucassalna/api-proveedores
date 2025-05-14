import requests
from django.conf import settings

class HTTPClient:
    @staticmethod
    def get(url, params=None, headers=None):
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=settings.API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post(url, data, headers=None):
        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=settings.API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()