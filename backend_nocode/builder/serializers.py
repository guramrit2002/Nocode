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
    is_published = serializers.BooleanField(write_only=True)

    class Meta:
        model = ProjectJson
        fields = ['project', 'json', 'is_published']

    def create(self, validated_data):
        project = validated_data["project"]
        is_published = validated_data.pop("is_published")
        json_data = validated_data["json"]

        project.is_published = is_published
        project.save(update_fields=["is_published"])

        project_json, _ = ProjectJson.objects.update_or_create(
            project=project,
            defaults={"json": json_data}
        )

        return project_json

    def update(self, instance, validated_data):
        project = instance.project
        is_published = validated_data.pop("is_published")
        json_data = validated_data.get("json")

        # Update Project
        project.is_published = is_published
        project.save(update_fields=["is_published"])

        # Update ProjectJson
        instance.json = json_data
        instance.save(update_fields=["json"])

        return instance
    
class JsonProjectSerializer(serializers.Serializer):
    
    is_published = serializers.BooleanField()
    json = serializers.JSONField()
