from rest_framework import serializers
from .models import Repositories, Events


class RepositorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Repository model.
    """

    class Meta:
        model = Repositories
        fields = ["id", "name", "owner"]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Event model.
    """

    class Meta:
        model = Events
        fields = ["id", "event_id", "event_type", "timestamp", "repository"]
