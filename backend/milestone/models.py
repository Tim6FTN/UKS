from django.db import models
from label.models import Label
from project.models import Project


class Milestone(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    labels = models.ManyToManyField(to=Label, blank=True)


    def __str__(self):
        return self.title
