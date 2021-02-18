from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from project.models import Project, Invite
from project.serializers import ProjectSerializer, InviteSerializer
from repository.models import Repository


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        if not (project.is_public or project.owner == request.user or project.collaborators.filter(
                id=request.user.id).exists()):
            raise PermissionDenied()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        if Project.objects.filter(owner=request.user, name=name).exists():
            raise ValidationError(f"Project with name {name} already exists")
        # Webhook for repository
        repository_url = request.data.get('repositoryUrl')

        repository = Repository.objects.create(name=name, url=repository_url)
        description = request.data['description']
        is_public = request.data.get('isPublic')
        project = Project.objects.create(name=name, repository=repository, description=description, is_public=is_public,
                                         owner=request.user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=request.data['id'])
        if project.owner != request.user:
            raise PermissionDenied()
        project.name = request.data['name']
        project.description = request.data['description']
        project.wiki_content = request.data['wiki_content'] if not None else project.wiki_content
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Returns project where user is owner or user is in collaborators
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        projects = Project.objects.filter(Q(collaborators__id=request.user.id) | Q(owner=request.user))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def star(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        project.stars.add(request.user)
        return Response()

    @action(detail=True)
    def removeStar(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        project.stars.remove(request.user)
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

        if user == request.user:
            raise ValidationError("You cannot invite yourself")

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
