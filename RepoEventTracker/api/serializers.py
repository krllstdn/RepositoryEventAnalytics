from rest_framework import serializers
from .models import Repositories, Events


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repositories
        fields = ["id", "name", "owner"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ["id", "event_id", "event_type", "timestamp", "repository"]
