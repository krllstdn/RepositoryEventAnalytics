from django.db import models


class Repositories(models.Model):
    """
    Represents a repository.

    Attributes:
        id (AutoField): The primary key of the repository.
        name (CharField): The name of the repository.
        owner (CharField): The owner of the repository.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Events(models.Model):
    """
    Represents an event in the system.

    Attributes:
        id (int): The unique primary key identifier for the event.
        event_id (int): The unique identifier for the event.
        event_type (str): The type of the event.
        timestamp (datetime): The timestamp of the event.
        repository (Repositories): The foreign key to the associated repository.
    """

    id = models.AutoField(primary_key=True)
    event_id = models.BigIntegerField(unique=True, null=True)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    repository = models.ForeignKey(Repositories, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_type
