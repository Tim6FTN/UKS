from django.contrib.auth.models import User
from django.db import models


class GithubProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=50)
