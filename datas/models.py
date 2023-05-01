from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class datas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    avatar = models.CharField(max_length=100,blank=True,null=True)
    