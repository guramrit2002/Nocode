from rest_framework import status as status_code

from .serializers import (UserProjectDashboardParamSerializer,
                          UserProjectDashboardSerializer)
from builder.models import Project

class UserProjectDashboardHandler:
    
    def get_dashboard_projects(self, request):
        
        params = request.query_params
        serializer = UserProjectDashboardParamSerializer(data=params)
        if not serializer.is_valid():
            return ("Invalid parameters", 
                    {"errors": serializer.errors}, 
                    status_code.HTTP_400_BAD_REQUEST)
        filters = serializer.data
        
        queryset = Project.objects.select_related('projectjson')\
            .filter(**filters)
        project_serializer = UserProjectDashboardSerializer(queryset, many=True)
        if not project_serializer.data:
            return ("No projects found", [], status_code.HTTP_200_OK)
        
        return ("Dashboard data fetched successfully", project_serializer.data, 
                status_code.HTTP_200_OK)