from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class jobsadmin(admin.ModelAdmin):
    list_display = ('surname','amount', 'created_at')