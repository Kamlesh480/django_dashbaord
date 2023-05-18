from django.contrib import admin
from .models import AutomationCredentials, UsersLogs, TeamMember, Group, Feedback

# Register your models here.
admin.site.register(AutomationCredentials)


class UsersLogsAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "user", "action", "description", "details"]


admin.site.register(UsersLogs, UsersLogsAdmin)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email"]
    search_fields = ["id", "name", "email"]


admin.site.register(TeamMember, TeamMemberAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "member_names", "user"]
    filter_horizontal = ["members"]
    search_fields = ["name", "members__name", "members__email", "user__username"]

    def member_names(self, obj):
        return ", ".join([member.name for member in obj.members.all()])

    member_names.short_description = "Members"


admin.site.register(Group, GroupAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["user", "feature", "created_at"]
    search_fields = ["user__username", "feature"]


admin.site.register(Feedback, FeedbackAdmin)
