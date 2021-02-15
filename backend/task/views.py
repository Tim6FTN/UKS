from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from task.serializers import TaskSerializer
from .models import Task

class TaskViewSet(viewsets.ModelViewSet):
  serializer_class= TaskSerializer
  queryset = Task.objects.all()

  def create(self, request):
    serializer_data = request.data
    serializer = self.serializer_class(data=serializer_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def retrieve(self, request, *args, **kwargs):
    serializer_instance = get_object_or_404(Task, id=kwargs.get('pk'))
    serializer = self.serializer_class(instance = serializer_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, *args, **kwargs):
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
  @action(detail=True)
  def open_task(self, *args, **kwargs):
    task = get_object_or_404(Task, id=kwargs.get('pk'))
    task.open_task()
    task.save()
    return Response()

  @action(detail=True)
  def close_task(self, *args, **kwargs):
    task = get_object_or_404(Task, id=kwargs.get('pk'))
    task.close_task()
    return Response()
