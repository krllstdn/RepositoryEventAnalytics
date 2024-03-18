from django.shortcuts import render
from rest_framework import generics
from .models import Repositories
from .models import Events
from .serializers import RepositorySerializer, EventSerializer
from .utils import fetch_and_save_repository_events
from rest_framework.views import APIView
from rest_framework.response import Response


class RepositoryListCreate(generics.ListCreateAPIView):
    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class EventListCreate(generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def delete(self, request):
        Events.objects.all().delete()
        return Response(status=204)


class FetchAndSaveRepositoryEvents(APIView):
    def get(self, request):
        try:
            fetch_and_save_repository_events()
        except Exception as e:
            return Response(
                {"error": f"Error fetching and saving events: {str(e)}"},
                status=500,
            )
        return Response(status=200)
