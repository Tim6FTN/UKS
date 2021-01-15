from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from project.models import Project
from project.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        userIds = [user.get('id') for user in request.data['users']]
        users = User.objects.filter(id__in=userIds)
        name = request.data['name']
        description = request.data['description']
        isPublic = request.data['isPublic']

        if Project.objects.filter(name=name).exists():
            raise ValidationError(f"Project with name: {name} already exists")

        project = Project.objects.create(name=name, description=description, isPublic=isPublic)
        project.users.set(users)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        userIds = [user.get('id') for user in request.data['users']]
        users = User.objects.filter(id__in=userIds)
        project = get_object_or_404(Project, id=request.data['id'])
        project.users.set(users)
        project.name = request.data['name']
        project.description = request.data['description']
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
