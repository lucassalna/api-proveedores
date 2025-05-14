from django.conf import settings
from .cliente import HTTPClient

class DispatchService:
    @staticmethod
    def send_provider_info(provider_data):
        """Send provider information to Dispatch API"""
        url = f"{settings.DISPATCH_API_URL}/providers"
        return HTTPClient.post(url, data=provider_data)

    @staticmethod
    def get_dispatch_status(dispatch_id):
        """Get dispatch status"""
        url = f"{settings.DISPATCH_API_URL}/dispatch/{dispatch_id}"
        return HTTPClient.get(url)