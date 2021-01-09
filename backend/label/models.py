from django.db import models


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7)
