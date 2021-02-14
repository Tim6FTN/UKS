from django.contrib.auth.models import User
from django.db import models

from repository.models import Repository


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    is_public = models.BooleanField(default=True)
    wiki_content = models.TextField(default='')
    repository = models.OneToOneField(to=Repository, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owner')
    stars = models.ManyToManyField(to=User, blank=True, related_name='stars')
    collaborators = models.ManyToManyField(to=User, blank=True, related_name='collaborators')

    def __str__(self):
        return self.name


# TODO: Should be added to UML model.
class Invite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project')
