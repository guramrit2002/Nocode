from django.db import models

# Create your models here.

class Project(models.Model):
    
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class ProjectJson(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.project.name
