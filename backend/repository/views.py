from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from repository.models import Repository, Invite
from repository.serializers import RepositorySerializer, InviteSerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def create(self, request, *args, **kwargs):
        # Owner = authenticated_user
        owner = get_object_or_404(User, id=request.data.get('owner').get('id'))
        name = request.data['name']
        description = request.data['description']

        if Repository.objects.filter(name=name).exists():
            raise ValidationError(f"Repository with name: {name} already exists")

        repository = Repository.objects.create(owner=owner, name=name, description=description)
        serializer = RepositorySerializer(repository)
        return Response(serializer.data)


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = InviteSerializer

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get('username'))
        repository = get_object_or_404(Repository, id=request.data.get('repositoryId'))
        invite = Invite.objects.create(user=user, repository=repository)
        serializer = InviteSerializer(invite)
        return Response(serializer.data)

