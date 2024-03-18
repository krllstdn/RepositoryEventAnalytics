from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Repository Event Tracker API",
        default_version="v1",
        description="A simple API to track events for GitHub repositories.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "statistics/",
        views.GetStatistics.as_view(),
        name="get-statistics",
    ),
    path(
        "fetch-events/",
        views.FetchAndSaveRepositoryEvents.as_view(),
        name="fetch-events",
    ),
    path(
        "repositories/",
        views.RepositoryListCreate.as_view(),
        name="repository-list-create",
    ),
    path(
        "repositories/<int:pk>/",
        views.RepositoryRetrieveUpdateDestroy.as_view(),
        name="repository-retrieve-update-destroy",
    ),
    path(
        "events/",
        views.EventListCreate.as_view(),
        name="event-list-create",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
