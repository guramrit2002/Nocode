import datetime
from copy import deepcopy
from django.conf import settings
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework import status
from .models import Project
from .serializers import (ProjectSerializer, CreateProjectSerializer, 
                        MarkPublishedSerializer, RequestParamsSerializer)

class ProjectHandler:
    
    def get_projects(self,request):
        try:
            params = deepcopy(request.query_params)
            if not params:
                projects = Project.objects.all()
                serializer = ProjectSerializer(projects, many=True)
            else:
                params_serializer = RequestParamsSerializer(data=params)
                if not params_serializer.is_valid():
                    print("Params errors:", params_serializer.errors)
                    return ("Invalid Query Parameters", {},
                            status.HTTP_400_BAD_REQUEST)
                filter_params = {}
                if 'is_published' in params_serializer.validated_data:
                    filter_params['is_published'] = \
                        params_serializer.validated_data['is_published']
                if 'created_at' in params_serializer.validated_data:
                    created_date = params_serializer.validated_data['created_at']
                    filter_params['created_at__date'] = created_date
                if 'id' in params_serializer.validated_data:
                    filter_params['id'] = params_serializer.validated_data['id']
                projects = Project.objects.filter(**filter_params)
                paginator = Paginator(projects,settings.PAGE_SIZE)
                paginator_page = params_serializer.validated_data.get('page',1)
                paginator_page_obj = paginator.get_page(paginator_page)
                serializer = ProjectSerializer(paginator_page_obj, many=True)
            return "Success", serializer.data, status.HTTP_200_OK
        except serializers.Serializer.errors as se:
            print(se)
            import traceback
            traceback.print_exc()
            return ("Serializer Error", {"error": str(se)},
                    status.HTTP_400_BAD_REQUEST)
    
    def post_project(self,request):
        
        try:
            data = deepcopy(request.data)
            serializer = CreateProjectSerializer(data=data)
            if serializer.is_valid():
                data = serializer.save()
                message = data.get("message")
                data.pop("message")
                print(message)
                if message:
                    return (message, {"data": data}, 
                        status.HTTP_201_CREATED)
                    
                return ("Project created", {"data": data}, 
                        status.HTTP_201_CREATED)
            else:
                return ("Serializer Error",{"errors": serializer.errors},
                        status.HTTP_400_BAD_REQUEST)
                        
        except Exception as e:
            return ("Something Went Wrong", {"error": str(e)},
                    status.HTTP_400_BAD_REQUEST)
    
    def put_project(self,request,pk):
        try:
            data = deepcopy(request.data)
            publish_serializer = MarkPublishedSerializer(data=data)
            if not publish_serializer.is_valid():
                if 'name' in request.data or 'created_at' in request.data:
                    return ("This API can only set projects as published", 
                            {},
                            status.HTTP_400_BAD_REQUEST)
                return ("Invalid Data", {},status.HTTP_400_BAD_REQUEST)
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project, data=request.data, 
                                           partial=True)
            if serializer.is_valid():
                serializer.save()
                return ("Project updated successfully", {"data": serializer.data},
                        status.HTTP_200_OK)
            else:
                return ("Serializer Error", {"errors": serializer.errors},
                        status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return ("Project not found", {}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return ("Something Went Wrong", {"error": str(e)},
                    status.HTTP_400_BAD_REQUEST)