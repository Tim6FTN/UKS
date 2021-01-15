from django.contrib.auth.models import User
from django.db import models
from milestone.models import Milestone
from project.models import Project

class Task(models.Model):
    priorities = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low")
    ]

    states = [
        ("Opened", "Opened"),
        ("Closed", "Closed")
    ]

    task_statuses = [
        ("ToDo", "ToDo"),
        ("InProgress", "InProgress"),
        ("Test", "Test"),
        ("Done", "Done")
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    date_opened = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, choices=priorities, default="Low")
    state = models.CharField(max_length=20, choices=states, default="Opened")
    task_status = models.CharField(max_length=20, choices=task_statuses, default="ToDo")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author')
    assignees = models.ManyToManyField(to=User, blank=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    milestone = models.ManyToManyField(to=Milestone, blank=True)

    def __str__(self):
        return self.title
