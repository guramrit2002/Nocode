from rest_framework import serializers
from .models import Project, ProjectJson

class ProjectSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Project
        fields = '__all__'
        
class CreateProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['name']
        
class MarkPublishedSerializer(serializers.Serializer):
    
    is_published = serializers.BooleanField(required=True)
    
class RequestParamsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(required=False)
    is_published = serializers.BooleanField(required=False)
    created_at = serializers.DateField(required=False)
    page = serializers.IntegerField(required=False)

class ProjectJsonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectJson
        fields = '__all__'
class SaveProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectJson
        fields = ['project', 'json']
        
    def create(self, validated_data):
        project_json_obj, created = ProjectJson.objects.update_or_create(
            project=validated_data['project'],
            defaults={'json': validated_data['json']}
        )
        return project_json_obj
    
class PublishProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectJson
        fields = ['project', 'json', 'html']
        
    def create(self, validated_data):
        project_json_obj, created = ProjectJson.objects.update_or_create(
            project=validated_data['project'],
            defaults={'json': validated_data['json'],
                      'html': validated_data.get('html', '')}
        )
        return project_json_obj