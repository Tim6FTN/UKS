from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from task.serializers import TaskSerializer
from .models import Task
from .models import Project


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get("project_pk"))

        serializer_context = {
          "author": request.user,
          "project": project
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        serializer_data = request.data
        serializer_instance = self.queryset.get(id=pk)

        assignees = serializer_data.get('assignees', None)
        if assignees is not None:
            print('AssigneeChange create')
            pass

        priority = serializer_data.get('priority', None)
        if priority is not None:
            print('PriorityChange create')
            pass

        taskStatus = serializer_data.get('status', None)
        if taskStatus is not None:
            print('StatusChange create')
            pass
        
        state = serializer_data.get('state', None)
        if state is not None:
            print('State create')
            pass
        
        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer_instance = get_object_or_404(Task, id=kwargs.get("pk"))
        serializer = self.serializer_class(instance=serializer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True)
    def open_task(self, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task.open_task()
        task.save()
        return Response()

    @action(detail=True)
    def close_task(self, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task.close_task()
        task.save()
        return Response()
