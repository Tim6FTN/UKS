from rest_framework import serializers
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from label.models import Label
from label.serializers import LabelSerializer
from milestone.models import Milestone
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'state', 'author']


class MilestoneSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    project_id = serializers.CharField()
    start_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    due_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, write_only=True,
                                                   required=False)
    task_set = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Milestone
        fields = ['id', 'project', 'title', 'description', 'start_date', 'due_date', 'labels', 'label_ids',
                  'project_id', 'task_set']

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Milestone.objects.all(),
                fields=('title', 'project_id'),
                message=_("Milestone with given title already exists")
            ),
        ]

    def validate(self, attrs):
        if attrs.get('due_date') < datetime.today().date():
            raise ValidationError(detail="Invalid due date.")

        return attrs

    def create(self, validated_data):
        project = self.context.get('project', None)
        start_date = datetime.now()

        labels = validated_data.pop('label_ids')

        milestone = Milestone.objects.create(project=project, start_date=start_date, **validated_data)
        milestone.labels.set(labels)
        return milestone

    def update(self, instance, validated_data):
        labels = validated_data.pop('label_ids')
        instance.first().labels.set(labels)
        return instance.update(**validated_data)
