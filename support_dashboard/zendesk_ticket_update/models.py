from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth.models import User


# Create your models here.
class Overview(models.Model):
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=500)


auditlog.register(Overview)


class ZendeskUpdateLogs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    status = models.TextField()
    description = models.TextField(default="")
    application = models.TextField()

    class Meta:
        ordering = ["-timestamp"]


auditlog.register(ZendeskUpdateLogs)
