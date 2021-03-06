from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Repository(models.Model):
    url = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Repositories")
