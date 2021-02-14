from rest_framework import serializers

from commit.models import Commit


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ['id']