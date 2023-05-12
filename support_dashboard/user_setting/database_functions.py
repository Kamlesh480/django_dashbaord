import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "support_dashboard.settings")
settings.configure()
import django

django.setup()

from user_setting.models import TeamMember
from .cred import all_members

for member_data in all_members:
    member = TeamMember(
        id=member_data["id"], name=member_data["name"], email=member_data["email"]
    )
    member.save()
