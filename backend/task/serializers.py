from datetime import datetime
from task.relations import UserRelatedField

from repository.serializers import UserSerializer
from rest_framework import serializers
from task.models import Task
from milestone.models import Milestone

class TaskSerializer(serializers.ModelSerializer):
  date_opened = serializers.SerializerMethodField(method_name='get_date_opened', read_only=True)
  date_closed = serializers.SerializerMethodField(method_name='get_date_closed', read_only=True)
  assignees = UserRelatedField(many=True, required=False)
  milestone = serializers.PrimaryKeyRelatedField(queryset=Milestone.objects.all(), many=True, required=False)


  class Meta:
    model = Task
    fields = (
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
      'milestone'
    )

  def create(self, validated_data):
    assignees = validated_data.pop('assignees', [])

    date_opened = datetime.now()

    task = Task.objects.create(
      date_opened=date_opened,
      **validated_data)
    for author in assignees:
      task.assignees.add(author)
    return task

  def get_date_opened(self, instance):
    return instance.date_opened.isoformat()
  
  def get_date_closed(self, instance):
    if instance.date_closed == None:
      return None
    return instance.date_closed.isoformat()
