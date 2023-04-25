from django.db import models
from django.contrib.auth.models import User


class AutomationCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    username = models.CharField(max_length=255)
    api_key = models.CharField(max_length=510)

    def __str__(self):
        return self.name
