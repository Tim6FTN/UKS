from change.serializers import AssignedMilestoneChangeSerializer, AssigneeChangeSerializer, CloseCommitReferenceSerializer, CommentSerializer, CommitReferenceSerializer, LabelChangeSerializer, PriorityChangeSerializer, StateChangeSerializer, StatusChangeSerializer
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from task.serializers import TaskSerializer

from .models import Task
from .models import Project
from change.models import AssignedMilestoneChange, AssigneeChange, CloseCommitReference, CommitReference, LabelChange, PriorityChange, StateChange, StatusChange, TaskChange, Comment, CREATE


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

    def list(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        tasks = Task.objects.filter(project_id=project_id)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post'], url_path='openTask')
    def open_task(self, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task.open_task()
        task.save()
        serializer = self.serializer_class(instance=task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='closeTask')
    def close_task(self, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task.close_task()
        task.save()
        serializer = self.serializer_class(instance=task)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], url_path='comment')
    def comments(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        if (request.method == "GET"):
            comments = Comment.objects.filter(task_id=task.id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            task = get_object_or_404(Task, id=kwargs.get("pk"))
            comment = Comment.objects.create(
                user = request.user,
                text = request.data.get('text', ''),
                change_type = CREATE,
                task = task
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='changes')
    def get_changes(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get("pk"))
        task_changes = TaskChange.objects.filter(task_id=task.id)
        response_data = []
        for change in task_changes:
            serialized_data = self.serialize_change(change)
            if serialized_data is None:
                continue
            response_data.append(serialized_data)
        return Response(response_data, status=status.HTTP_200_OK)

    def serialize_change(self, change):
        if isinstance(change, CloseCommitReference):
            serializer = CloseCommitReferenceSerializer(change)
            return serializer.data
        elif isinstance(change, CommitReference):
            serializer = CommitReferenceSerializer(change)
            return serializer.data
        elif isinstance(change, AssigneeChange):
            serializer = AssigneeChangeSerializer(change)
            return serializer.data
        elif isinstance(change, LabelChange):
            serializer = LabelChangeSerializer(change)
            return serializer.data
        elif isinstance(change, PriorityChange):
            serializer = PriorityChangeSerializer(change)
            return serializer.data
        elif isinstance(change, StatusChange):
            serializer = StatusChangeSerializer(change)
            return serializer.data
        elif isinstance(change, StateChange):
            serializer = StateChangeSerializer(change)
            return serializer.data
        elif isinstance(change, AssignedMilestoneChange):
            serializer = AssignedMilestoneChangeSerializer(change)
            return serializer.data
        return None

