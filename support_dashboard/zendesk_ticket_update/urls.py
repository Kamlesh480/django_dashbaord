from django.urls import path, include
from . import views
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path("", views.login, name="login"),
    path("login", RedirectView.as_view(permanent=True, url="/")),
    path("register", RedirectView.as_view(permanent=True, url="/")),
    # path("register", views.register, name="register"),
    path("home", views.home, name="home"),
    path("update_zendesk", views.update_zendesk, name="update_zendesk"),
]
