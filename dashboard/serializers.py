from rest_framework import serializers
from builder.models import Project

class UserProjectDashboardParamSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField()
    is_published = serializers.BooleanField()

class UserProjectDashboardSerializer(serializers.ModelSerializer):
    
    json = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'is_published', 'url', 'created_at', 
                  'json')

    def get_json(self, obj):
        if hasattr(obj, "projectjson"):
            return obj.projectjson.json
        return None