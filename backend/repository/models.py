from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Repository(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    stars = models.ManyToManyField(to=User, blank=True, related_name='stars')
    users = models.ManyToManyField(to=User, blank=True, related_name='users')
    isPublic = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Repositories")


class Invite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE, related_name='repository')
