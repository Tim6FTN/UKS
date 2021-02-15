from rest_framework import serializers
from django.contrib.auth.models import User

from milestone.models import Milestone

class UserRelatedField(serializers.RelatedField):

  class Meta:
    model = User

  def get_queryset(self):
      return User.objects.all()

  def to_internal_value(self, data):
    print("to_internal", data)
    user = User.objects.get(username=data)
    return User.objects.get(username=data)

  def to_representation(self, value):
    print("to_representation", value.__dict__)
    return value.username

class MilestoneRelatedField(serializers.RelatedField):

  class Meta:
    model = Milestone

  def get_queryset(self):
      return Milestone.objects().all()

  def to_representation(self, value):
      return value.id