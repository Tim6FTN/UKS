from django.db import models

from label.models import Label
from project.models import Project


class Milestone(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey(to=Project, null=False, on_delete=models.CASCADE)
    labels = models.ManyToManyField(to=Label, blank=True)

    def __str__(self):
        return self.title
