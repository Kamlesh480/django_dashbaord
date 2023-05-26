from django.contrib import admin
from .models import Overview, ZendeskUpdateLogs, TestModel


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


class TestModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(TestModel, TestModelAdmin)
# admin.site.unregister(TestModel)
