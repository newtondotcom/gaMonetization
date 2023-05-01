from django.contrib import admin
from .models import payout

# Register your models here.
@admin.register(payout)
class payoutadmin(admin.ModelAdmin):
    list_display = ('amount', 'created_at', 'paid_at', 'status', 'user')