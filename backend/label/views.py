from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from label.models import Label
from label.serializers import LabelSerializer
from project.models import Project


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))
        labels = project.label_set
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('project_pk'))
        label = Label.objects.create(name=request.data.get('name'), color=request.data.get('color'), project=project)
        serializer = LabelSerializer(label)
        return Response(serializer.data)