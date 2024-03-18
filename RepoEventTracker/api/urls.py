from django.urls import path
from . import views

urlpatterns = [
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
        "fetch-events/",
        views.FetchAndSaveRepositoryEvents.as_view(),
        name="fetch-events",
    ),
    path(
        "statistics/",
        views.GetStatistics.as_view(),
        name="get-statistics",
    ),
]
