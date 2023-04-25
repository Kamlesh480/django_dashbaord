from django.urls import path
from . import views

urlpatterns = [
    path("settings", views.user_settings, name="user_settings"),
    path("settings_fun_calls", views.settings_fun_calls, name="settings_fun_calls"),
]
