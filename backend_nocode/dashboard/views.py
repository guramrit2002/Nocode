from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from backend_nocode.utils import response
from rest_framework import status as status_code
from .handlers import UserProjectDashboardHandler
# Create your views here.

class UserProjectDashboardViewSet(ViewSet):
    
    def list(self, request):
        try:
            obj = UserProjectDashboardHandler()
            message, data, status = obj.get_dashboard_projects(request)
            return response(message=message, 
                            data=data, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)},
                            status=status_code.HTTP_500_INTERNAL_SERVER_ERROR)
