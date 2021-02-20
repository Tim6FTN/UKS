from django.contrib.auth.models import User
from django.db import models

from branch.models import Branch


class CommitMetaData(models.Model):
    file_additions_count = models.IntegerField(default=0)
    file_deletions_count = models.IntegerField(default=0)
    file_modifications_count = models.IntegerField(default=0)
    line_additions_count = models.IntegerField(default=0)
    line_deletions_count = models.IntegerField(default=0)
    line_modifications_count = models.IntegerField(default=0)


class Commit(models.Model):
    author_username = models.CharField(max_length=100)
    hash_id = models.CharField(max_length=100)
    message = models.TextField()
    description = models.CharField(max_length=400, default='')
    url = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    commit_meta_data = models.OneToOneField(to=CommitMetaData, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
