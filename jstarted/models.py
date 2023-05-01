from django.db import models
from jobs.models import Job
from django.contrib.auth.models import User

# Create your models here.
class jstarted(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taken_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
