from django.contrib.auth.models import User
from django.db import models
from repository.models import Repository


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    repository = models.OneToOneField(to=Repository, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
