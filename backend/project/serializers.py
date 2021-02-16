from django.contrib.auth.models import User
from rest_framework import serializers

from project.models import Project, Invite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    stars = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'description', 'repository', 'stars', 'is_public', 'wiki_content']


class InviteProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class InviteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = InviteProjectSerializer(read_only=True)

    class Meta:
        model = Invite
        fields = ['id', 'user', 'project']
