from django.contrib import admin
from .models import AutomationCredentials, UsersLogs

# Register your models here.
admin.site.register(AutomationCredentials)


class UsersLogsAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "user", "action", "description", "details"]


admin.site.register(UsersLogs, UsersLogsAdmin)
