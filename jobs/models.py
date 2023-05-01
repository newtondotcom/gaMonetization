from django.db import models

# Create your models here.
class Job(models.Model):
    link = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=100)
    surname = models.CharField(max_length=100,blank=True,null=True)