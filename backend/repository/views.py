from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from repository.models import Repository
from repository.serializers import RepositorySerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def create(self, request, *args, **kwargs):
        # Owner = authenticated_user
        owner = get_object_or_404(User, id=request.data.get('owner').get('id'))
        name = request.data['name']
        description = request.data['description']
        is_public = request.data['isPublic']

        if Repository.objects.filter(name=name).exists():
            raise ValidationError(f"Repository with name: {name} already exists")

        repository = Repository.objects.create(owner=owner, name=name, description=description, isPublic=is_public)
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Check if authenticated user is owner of repository
        repository = get_object_or_404(Repository, id=kwargs.get('pk'))
        repository.name = request.data.get('name')
        repository.description = request.data.get('description')
        saved = repository.save()
        serializer = RepositorySerializer(saved)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # filter by user, include private repositories
        # queryset = User.objects.filter(user=logged_user)
        queryset = Repository.objects.all()
        serializer = RepositorySerializer(queryset, many=True)
        return Response(serializer.data)
