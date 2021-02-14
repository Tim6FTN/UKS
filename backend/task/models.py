from django.contrib.auth.models import User
from django.db import models

from label.models import Label
from milestone.models import Milestone
from project.models import Project

PRIORITIES = [
    ("NotAssigned", "NotAssigned"),
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low")
]

STATES = [
    ("Open", "Open"),
    ("Closed", "Closed")
]

TASK_STATUSES = [
    ("Backlog", "Backlog"),
    ("ToDo", "ToDo"),
    ("InProgress", "InProgress"),
    ("Done", "Done")
]


class Task(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(null=True)
    priority = models.CharField(max_length=20, choices=PRIORITIES, default="NotAssigned")
    state = models.CharField(max_length=20, choices=STATES, default="Open")
    task_status = models.CharField(max_length=20, choices=TASK_STATUSES, default="Backlog")
    attachment = models.FileField(null=True, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    milestone = models.ForeignKey(to=Milestone, null=True, blank=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(to=Label, blank=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author')
    assignees = models.ManyToManyField(to=User, blank=True)

    def __str__(self):
        return self.title
