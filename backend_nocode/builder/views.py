import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .handlers import ProjectHandler
from backend_nocode.utils import response
# Create your views here.


class ProjectViewSet(ViewSet):
    
    def list(self, request):
        try:
            obj = ProjectHandler()
            message, date, status = obj.get_projects(request)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)})
    
    def create(self,request):
        try:
            obj = ProjectHandler()
            message, date, status = obj.post_project(request)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)})
    