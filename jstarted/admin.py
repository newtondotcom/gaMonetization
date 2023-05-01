from django.contrib import admin
from .models import jstarted

# Register your models here.
@admin.register(jstarted)
class jstartedadmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'taken_at', 'done')