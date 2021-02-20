from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from integration.importer import RepositoryImporter
from project.models import Project, Invite
from project.serializers import ProjectSerializer, InviteSerializer


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
        name = request.data.get('name', '')
        if Project.objects.filter(owner=request.user, name=name).exists():
            raise ValidationError(f"Project with name {name} already exists")

        repository_url = request.data.get('repositoryUrl', None)
        if repository_url is None or repository_url.isspace() or repository_url == "":
            raise ValidationError()

        repository_importer = RepositoryImporter(repository_url=repository_url)
        repository_importer.check_if_repository_exists()
        repository = repository_importer.import_repository()

        serializer_context = {
            "owner": request.user,
            "repository": repository
        }

        serializer = self.serializer_class(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer_context = {
            "owner": request.user,
            "method": request.method
        }
        pk = kwargs.get('pk')
        project = get_object_or_404(Project, id=pk)

        if project.owner != request.user:
            raise PermissionDenied()

        name = request.data.get('name', '')
        if project.name != name and Project.objects.filter(owner=request.user, name=name):
            raise ValidationError(f"Project with name {name} already exists")

        serializer = self.serializer_class(
            project,
            data=request.data,
            context=serializer_context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        projects = Project.objects.filter(Q(collaborators__id=request.user.id) | Q(owner=request.user))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        if project.owner != request.user:
            raise PermissionDenied()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    http_method_names = ['get', 'post', 'delete']

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
            raise PermissionDenied()
        invite.project.collaborators.add(invite.user)
        invite.delete()
        return Response()

    def list(self, request, *args, **kwargs):
        invites = Invite.objects.filter(user=request.user)
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        invite = get_object_or_404(Invite, pk=kwargs.get('pk'))
        if invite.user != request.user:
            raise PermissionDenied()
        invite.delete()
        return Response()

