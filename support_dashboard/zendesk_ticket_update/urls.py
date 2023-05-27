from django.urls import path, include
from . import views
from . import analyzer_views
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path("", views.login, name="login"),
    path("login", RedirectView.as_view(permanent=True, url="/")),
    path("register", RedirectView.as_view(permanent=True, url="/")),
    # path("register", views.register, name="register"),
    path("home", views.home, name="home"),
    path("update_zendesk", views.update_zendesk, name="update_zendesk"),
    path("slack_message", views.slack_message, name="slack_message"),
    # Issue analyzer
    path("issue_analyzer", analyzer_views.issue_analyzer, name="issue_analyzer"),
    path(
        "get_pipeline_detail",
        analyzer_views.get_pipeline_detail,
        name="get_pipeline_detail",
    ),
]
