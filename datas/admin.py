from django.contrib import admin
from .models import datas

# Register your models here.
@admin.register(datas)
class DatasAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')