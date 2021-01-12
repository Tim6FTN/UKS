from rest_framework import serializers

from label.models import Label


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color']
