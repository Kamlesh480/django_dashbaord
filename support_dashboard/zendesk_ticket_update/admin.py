from django.contrib import admin
from .models import Overview, ZendeskUpdateLogs


# Register your models here.
admin.site.register(Overview)


class ZendeskUpdateLogsAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
        "user",
        "action",
        "status",
        "description",
        "application",
    ]


admin.site.register(ZendeskUpdateLogs, ZendeskUpdateLogsAdmin)
