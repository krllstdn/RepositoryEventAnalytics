from django.db import models


class Repositories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Events(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.BigIntegerField(unique=True, null=True)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    repository = models.ForeignKey(Repositories, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_type
