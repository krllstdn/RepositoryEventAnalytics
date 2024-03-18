from django.shortcuts import render
from rest_framework import generics
from .models import Repositories
from .models import Events
from .serializers import RepositorySerializer, EventSerializer
from .utils import fetch_and_save_repository_events, get_statistics
from rest_framework.views import APIView
from rest_framework.response import Response


class RepositoryListCreate(generics.ListCreateAPIView):
    """List all repositories or create a new repository."""

    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a repository."""

    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class EventListCreate(generics.ListCreateAPIView):
    """List all events or create a new event."""

    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def delete(self, request):
        """Delete all events."""
        Events.objects.all().delete()
        return Response(status=204)


class FetchAndSaveRepositoryEvents(APIView):
    """Fetch and save repository events to the database."""

    def get(self, request):
        """
        Handle GET requests.

        This method fetches and saves repository events. If an error occurs during the process,
        an error response with the corresponding error message is returned. Otherwise, a success
        response with a status code of 200 is returned.

        Returns:
            A Response object with a status code of 200 if successful, or an error response with
            a status code of 500 if an error occurs.
        """
        try:
            fetch_and_save_repository_events()
        except Exception as e:
            return Response(
                {"error": f"Error fetching and saving events: {str(e)}"},
                status=500,
            )
        return Response(status=200)


class GetStatistics(APIView):
    """Retrieve statistics."""

    def get(self, request):
        """
        Retrieve statistics.

        This method retrieves statistics using the `get_statistics` function.
        If an error occurs during the retrieval process, an error response with
        the corresponding error message is returned. Otherwise, a success response
        with the retrieved statistics is returned.

        Returns:
            A Response object with the retrieved statistics and a status code.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            statistics = get_statistics()
        except Exception as e:
            return Response(
                {"error": f"Error getting statistics: {str(e)}"},
                status=500,
            )
        return Response(
            statistics,
            status=200,
        )
