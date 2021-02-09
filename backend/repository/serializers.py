from django.contrib.auth.models import User
from rest_framework import serializers

from repository.models import Repository


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'username': {
                'validators': [],
            }
        }


class RepositorySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    stars = UserSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = ['id', 'owner', 'name', 'description', 'stars', 'users', 'isPublic', 'project']

    def create(self, validated_data):
        print("asdasdasdasda")
        print(self.context['owner'])
        print(validated_data)
        owner = self.context['owner']
        return Repository.objects.create(
            owner=owner, **validated_data
        )
