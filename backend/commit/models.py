from django.db import models
from branch.models import Branch


class Commit(models.Model):
    hash = models.CharField(max_length=100)
    message = models.CharField(max_length=400)
    timestamp = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
