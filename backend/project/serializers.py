from django.contrib.auth.models import User
from rest_framework import serializers
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'repository']


