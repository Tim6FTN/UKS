from django.db import models
from milestone.models import Milestone
from task.models import Task


class Change(models.Model):
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class MilestoneChange(Change):
    milestone = models.ForeignKey(to=Milestone, on_delete=models.CASCADE)


class TaskChange(Change):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)