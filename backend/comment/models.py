from django.contrib.auth.models import User
from django.db import models

from task.models import Task


class Comment(models.Model):
    text = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(null=True, blank=True)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
