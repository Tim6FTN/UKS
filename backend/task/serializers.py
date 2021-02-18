from datetime import datetime
from milestone.serializer import MilestoneSerializer
from project.serializers import ProjectSerializer, UserSerializer
from task.relations import UserRelatedField

from rest_framework import serializers
from task.models import Task
from milestone.models import Milestone
from label.models import Label
from label.serializers import LabelSerializer

class TaskSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  date_opened = serializers.SerializerMethodField(method_name='get_date_opened', read_only=True)
  date_closed = serializers.SerializerMethodField(method_name='get_date_closed', read_only=True)
  assignees = UserRelatedField(many=True, required=False)
  milestone = serializers.PrimaryKeyRelatedField(queryset=Milestone.objects.all(), required=False, write_only=True)
  labels = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, required=False, write_only=True)
  labelsInfo = LabelSerializer(source='labels', many=True, read_only=True)
  milestoneInfo = MilestoneSerializer(source='milestone', read_only=True)

  project = serializers.CharField(source='project.id', read_only=True)


  class Meta:
    model = Task
    fields = (
      'id',
      'title',
      'description',
      'attachment',
      'priority',
      'state',
      'task_status',
      'author',
      'assignees',
      'date_opened',
      'date_closed',
      'project',
      'milestone',
      'labels',
      'labelsInfo',
      'milestoneInfo'
    )

  def create(self, validated_data):
    assignees = validated_data.pop('assignees', [])
    labels = validated_data.pop('labels', [])

    author = self.context.get('author', None)
    project = self.context.get('project', None)

    date_opened = datetime.now()
    task = Task.objects.create(
      author=author,
      project=project,
      date_opened=date_opened,
      **validated_data)

    for author in assignees:
      task.assignees.add(author)

    for label in labels:
      task.labels.add(label)

    return task

  def get_date_opened(self, instance):
    return instance.date_opened.isoformat()
  
  def get_date_closed(self, instance):
    if instance.date_closed == None:
      return None
    return instance.date_closed.isoformat()
