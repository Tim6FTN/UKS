from commit.serializers import CommitSerializer
from project.serializers import UserSerializer
from rest_framework import serializers

from change.models import AssignedMilestoneChange, AssigneeChange, CloseCommitReference, Comment, CommentEdit, CommitReference, LabelChange, PriorityChange, TaskChange
from milestone.serializer import MilestoneSerializer
from label.serializers import LabelSerializer

class TaskChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = TaskChange
    fields = ('timestamp', 'change_type', 'description', 'user')

class CloseCommitReferenceSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  closing_commit = CommitSerializer(source='referenced_commit')

  class Meta:
    model = CloseCommitReference
    fields = ('timestamp', 'change_type', 'description', 'user', 'closing_commit')

class CommitReferenceSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  referenced_commit = CommitSerializer()

  class Meta:
    model = CommitReference
    fields = ('timestamp', 'change_type', 'description', 'user', 'referenced_commit')


class AssigneeChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  assignee = UserSerializer()

  class Meta:
    model = AssigneeChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'assignee')

class LabelChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  label = LabelSerializer()

  class Meta:
    model = LabelChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'label')


class PriorityChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = PriorityChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'old_priority', 'new_priority')


class StatusChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = TaskChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'old_status', 'new_status')


class StateChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = TaskChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'new_state')

class AssignedMilestoneChangeSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  milestone = MilestoneSerializer()

  class Meta:
    model = AssignedMilestoneChange
    fields = ('timestamp', 'change_type', 'description', 'user', 'milestone')

class CommentEditSerializer(serializers.ModelSerializer):

  class Meta:
    model=CommentEdit
    fields = ('text', 'timestamp')


class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer(source='user')
  edits = CommentEditSerializer(source='commentedit_set', many=True, read_only=True)
  
  class Meta:
    model=Comment
    fields = ('author', 'text', 'timestamp', 'edits')
