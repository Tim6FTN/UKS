from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from label.serializers import LabelSerializer
from project.models import Project, Invite
from project.serializers import ProjectSerializer, InviteSerializer
from repository.models import Repository


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        # Webhook for repository
        repository = Repository.objects.create(name=request.data.get('repositoryUrl'),
                                               url=request.data.get('repositoryUrl'))
        description = request.data['description']
        is_public = request.data.get('isPublic')
        project = Project.objects.create(name=name, repository=repository, description=description, is_public=is_public,
                                         owner=request.user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=request.data['id'])
        project.name = request.data['name']
        project.description = request.data['description']
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def star(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        project.stars.add(request.user)
        return Response()

    @action(detail=False, permission_classes=[AllowAny])
    def getTopFive(self, *args, **kwargs):
        projects = Project.objects.filter(is_public=True).annotate(star_count=Count('stars')).order_by('-star_count')[
                   :5]
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[AllowAny])
    def search(self, *args, **kwargs):
        search_param = self.request.query_params.get("value")
        projects = Project.objects.filter(name__contains=search_param, is_public=True).annotate(
            star_count=Count('stars')).order_by('-star_count')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get('username'))
        project = get_object_or_404(Project, id=request.data.get('projectId'))
        if project.owner.id != request.user.id:
            raise ValidationError("You are not owner of the project")

        invite = Invite.objects.create(user=user, project=project)
        serializer = InviteSerializer(invite)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        invite = get_object_or_404(Invite, pk=kwargs.get('pk'))
        if invite.user_id != request.user.id:
            raise ValidationError(code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        invite.project.collaborators.add(invite.user)
        invite.delete()
        return Response()
