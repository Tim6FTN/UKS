from django.contrib.auth.models import User
from django.db import models
from project.models import Project
from django.utils.translation import gettext_lazy as _


class Repository(models.Model):
    url = models.CharField(max_length=100)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)
    stars = models.ManyToManyField(to=User, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name_plural = _("Repositories")
