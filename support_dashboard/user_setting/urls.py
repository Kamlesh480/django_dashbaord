from django.urls import path
from . import views

urlpatterns = [
    path("settings", views.user_settings, name="user_settings"),
    path("add_credentials", views.add_credentials, name="add_credentials"),
]
