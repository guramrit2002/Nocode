import datetime
from rest_framework import serializers
from .models import Project, ProjectJson

class ProjectSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Project
        fields = '__all__'
        
class CreateProjectSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=200,required=True)
    json = serializers.JSONField()
    
    
    def create(self, validated_data):
        project, not_exists = Project.objects.get_or_create(
            name = validated_data.get("name")
        )
        json_p, is_json_created = ProjectJson.objects.get_or_create(
            project = project,
            json = validated_data.get("json")
        )
        
        response = {
            "project_id":project.id,
            "project_name":project.name,
            "project_json":json_p.json
        }
        
        if not not_exists:
            response.update({"message":"Project with same name already exists"})
            
        return response

class MarkPublishedSerializer(serializers.Serializer):
    
    is_published = serializers.BooleanField(required=True)
    
class RequestParamsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(required=False)
    is_published = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False)