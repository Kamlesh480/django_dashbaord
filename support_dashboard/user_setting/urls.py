from django.urls import path
from . import views

urlpatterns = [
    path("settings", views.settings, name="settings"),
    path("settings_fun_calls", views.settings_fun_calls, name="settings_fun_calls"),
]
