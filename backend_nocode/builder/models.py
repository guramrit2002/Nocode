from django.db import models

# Create your models here.

class Project(models.Model):
    
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    url = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.name
    
class ProjectJson(models.Model):
    project = models.OneToOneField(Project,on_delete=models.CASCADE)
    json = models.JSONField()
    html = models.TextField(default="",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.project.name
