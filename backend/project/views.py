from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from project.models import Project
from project.serializers import ProjectSerializer
from repository.models import Repository


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        description = request.data['description']
        repository = get_object_or_404(Repository, id=request.data['repository'])

        if Project.objects.filter(name=name).exists():
            raise ValidationError(f"Project with name: {name} already exists")

        project = Project.objects.create(name=name, description=description, repository=repository)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=request.data['id'])
        project.name = request.data['name']
        project.description = request.data['description']
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
