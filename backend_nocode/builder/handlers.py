import datetime
from copy import deepcopy
from rest_framework import serializers
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer, CreateProjectSerializer

class ProjectHandler:
    
    def get_projects(self,request):
        try:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return "Success", serializer.data, status.HTTP_200_OK
        except serializers.Serializer.errors as se:
            print(se)
            import traceback
            traceback.print_exc()
            return ("Serializer Error", {"error": str(se)},
                    status.HTTP_400_BAD_REQUEST)
    
    def post_project(self,request):
        
        try:
            serializer = CreateProjectSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                message = data.get("message")
                print(message)
                if message:
                    return (message, {"project": data}, 
                        status.HTTP_201_CREATED)
                    
                return ("Project created", {"project": data}, 
                        status.HTTP_201_CREATED)
            else:
                return ("Serializer Error",{"errors": serializer.errors},
                        status.HTTP_400_BAD_REQUEST)
                        
        except Exception as e:
            return ("Something Went Wrong", {"error": str(e)},
                    status.HTTP_400_BAD_REQUEST)