from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(to=User, blank=True)
    description = models.TextField(null=True, blank=True)
    isPublic = models.BooleanField(default=True)

    def __str__(self):
        return self.name
