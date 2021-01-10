from django.db import models


class Wiki(models.Model):
    content = models.TextField()
