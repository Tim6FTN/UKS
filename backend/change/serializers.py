from project.serializers import UserSerializer
from rest_framework import serializers

from change.models import Comment, CommentEdit

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
