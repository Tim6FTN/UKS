from django.contrib.auth.models import User
from rest_framework import serializers

from project.models import Invite
from repository.models import Repository


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RepositorySerializer(serializers.ModelSerializer):
    # owner = UserSerializer(read_only=True)
    # stars = UserSerializer(many=True, read_only=True)
    # users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = ['id', 'name', 'description', 'is_public', 'project']


class InviteRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name']


class InviteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    repository = InviteRepositorySerializer(read_only=True)

    class Meta:
        model = Invite
        fields = ['id', 'user', 'repository']
