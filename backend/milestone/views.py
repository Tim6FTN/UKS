# Create your views here.
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from milestone.models import Milestone
from milestone.serializer import MilestoneSerializer
from project.models import Project


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))
        if project.owner != request.user and not project.collaborators.all().filter(
                username=request.user.username).exists():
            raise PermissionDenied()

        context = {
            "project": project
        }

        serializer_data = request.data | {"project_id": project.id}
        serializer = self.serializer_class(
            data=serializer_data, context=context,
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))

        if project.owner != request.user and not project.collaborators.all().filter(
                username=request.user.username).exists():
            raise PermissionDenied()

        context = {
            "project": project
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=context
        )
        serializer.validators = []
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))

        if project.owner != request.user and not project.collaborators.all().filter(
                username=request.user.username).exists():
            raise PermissionDenied()

        milestones = Milestone.objects.filter(project=project)
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))

        if project.owner != request.user and not project.collaborators.all().filter(
                username=request.user.username).exists():
            raise PermissionDenied()

        milestone = get_object_or_404(Milestone, pk=kwargs.get('pk'))
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
