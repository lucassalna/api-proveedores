from django.conf import settings
from .cliente import HTTPClient

class RequisitionService:
    @staticmethod
    def get_required_materials():
        """Get required materials from Requisition API"""
        url = f"{settings.REQUISITION_API_URL}/materials"
        return HTTPClient.get(url)

    @staticmethod
    def get_requisition_details(requisition_id):
        """Get specific requisition details"""
        url = f"{settings.REQUISITION_API_URL}/requisitions/{requisition_id}"
        return HTTPClient.get(url)