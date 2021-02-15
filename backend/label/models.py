from django.core.validators import RegexValidator
from django.db import models

from project.models import Project


class Label(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, validators=[RegexValidator(regex='^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$',
                                                                      message="Hex color doesn't match pattern")])

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name',)
