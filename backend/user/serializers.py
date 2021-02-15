from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import GithubProfile


class GithubProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubProfile
        fields = ['id', 'github_username']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    github_username = serializers.CharField(write_only=True)
    github_profile = GithubProfileSerializer(source='githubprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'github_username', 'github_profile']

    def create(self, validated_data):
        github_username = validated_data.pop('github_username')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        GithubProfile.objects.create(github_username=github_username, user=user)
        return user
