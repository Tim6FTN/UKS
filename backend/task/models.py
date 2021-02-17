from django.contrib.auth.models import User
from django.db import models

from label.models import Label
from datetime import datetime

from milestone.models import Milestone
from project.models import Project

NOT_ASSIGNED = "NotAssigned"
HIGH = "High"
MEDIUM = "Medium"
LOW = "Low"
PRIORITIES = [
    (NOT_ASSIGNED, "NotAssigned"),
    (HIGH, "High"),
    (MEDIUM, "Medium"),
    (LOW, "Low")
]

OPEN = "Open"
CLOSED = "Closed"
STATES = [
    (OPEN, "Open"),
    (CLOSED, "Closed")
]

BACKLOG = "Backlog"
TODO = "ToDo"
IN_PROGRESS = "InProgress"
DONE = "Done"
TASK_STATUSES = [
    (BACKLOG, "Backlog"),
    (TODO, "ToDo"),
    (IN_PROGRESS, "InProgress"),
    (DONE, "Done")
]


class Task(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField(null=True)
    priority = models.CharField(max_length=20, choices=PRIORITIES, default=NOT_ASSIGNED)
    state = models.CharField(max_length=20, choices=STATES, default=OPEN)
    task_status = models.CharField(max_length=20, choices=TASK_STATUSES, default=BACKLOG)
    attachment = models.FileField(null=True, blank=True)
    project = models.ForeignKey(to=Project, null=False, on_delete=models.CASCADE)
    milestone = models.ForeignKey(to=Milestone, null=True, blank=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(to=Label, blank=True)
    author = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE, related_name='author')
    assignees = models.ManyToManyField(to=User, blank=True)

    def open_task(self):
        self.state = "Open"
        self.date_opened = datetime.now()
        self.date_closed = None

    def close_task(self):
        self.state = 'Closed'
        self.date_closed = datetime.now()

    def __str__(self):
        return self.title
