import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status as status_code
from .handlers import ProjectHandler
from backend_nocode.utils import response
# Create your views here.


class ProjectViewSet(ViewSet):
    
    def list(self, request):
        try:
            obj = ProjectHandler()
            message, date, status = obj.get_projects(request)
            print("response from hanldler", message, date, status)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)},
                            status=status_code.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self,request):
        try:
            obj = ProjectHandler()
            message, date, status = obj.post_project(request)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)})
    
    def update(self,request,pk):
        try:
            obj = ProjectHandler()
            message, date, status = obj.put_project(request,pk)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)})
        
    def retrieve(self,request,pk):
        try:
            obj = ProjectHandler()
            message, date, status = obj.get_projects(request,pk)
            return response(message=message, data=date, status=status)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return response("Something Went wrong",{"error": str(e)})
    