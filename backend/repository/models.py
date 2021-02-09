from django.contrib.auth.models import User
from django.db import models
from project.models import Project
from django.utils.translation import gettext_lazy as _

from project.models import Project


class Repository(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stars = models.ManyToManyField(to=User, blank=True, related_name='stars')
    users = models.ManyToManyField(to=User, blank=True, related_name='users')
    isPublic = models.BooleanField(default=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project', null=True, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name_plural = _("Repositories")
