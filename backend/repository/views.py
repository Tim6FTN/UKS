from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
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
        isPublic = request.data['isPublic']

        if Repository.objects.filter(name=name).exists():
            raise ValidationError(f"Repository with name: {name} already exists")

        repository = Repository.objects.create(owner=owner, name=name, description=description, isPublic=isPublic)
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

    @action(detail=True)
    def star(self, *args, **kwargs):
        # Change to authenticated user
        user = User.objects.all().first()
        repository = get_object_or_404(Repository, id=kwargs.get('pk'))
        repository.stars.add(user)
        return Response()

    @action(detail=False)
    def search(self, *args, **kwargs):
        search_param = self.request.query_params.get("value")
        repositories = Repository.objects.filter(name__contains=search_param, isPublic=True).annotate(star_count=Count('stars')).order_by('-star_count')
        serializer = RepositorySerializer(repositories, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def getTopFive(self, *args, **kwargs):
        repositories = Repository.objects.filter(isPublic=True).annotate(star_count=Count('stars')).order_by('-star_count')[:5]
        serializer = RepositorySerializer(repositories, many=True)
        return Response(serializer.data)


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get('username'))
        repository = get_object_or_404(Repository, id=request.data.get('repositoryId'))
        # Check if user is owner of repository else return bad request
        invite = Invite.objects.create(user=user, repository=repository)
        serializer = InviteSerializer(invite)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        invite = get_object_or_404(Invite, pk=kwargs.get('pk'))
        invite.repository.users.add(invite.user)
        invite.delete()
        return Response()
