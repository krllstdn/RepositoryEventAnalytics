from django.shortcuts import render
from rest_framework import generics
from .models import Repositories
from .serializers import RepositorySerializer


class RepositoryListCreate(generics.ListCreateAPIView):
    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer


class EventListCreate(generics.ListCreateAPIView):
    queryset = Repositories.objects.all()
    serializer_class = RepositorySerializer
