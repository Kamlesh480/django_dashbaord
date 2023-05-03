from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog


class AutomationCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    api_key = models.CharField(max_length=510)

    def __str__(self):
        return self.name


auditlog.register(AutomationCredentials)


class UsersLogs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]


auditlog.register(UsersLogs)
