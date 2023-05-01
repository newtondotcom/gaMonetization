from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class payout(models.Model):
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username