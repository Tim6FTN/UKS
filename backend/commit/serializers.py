from rest_framework import serializers

from commit.models import Commit, CommitMetaData

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitMetaData
        fields = ['file_additions_count', 'file_deletions_count', 'file_modifications_count', 'line_additions_count', 'line_deletions_count', 'line_modifications_count']

class CommitSerializer(serializers.ModelSerializer):
    commit_meta_data = MetaDataSerializer(read_only=True)
    class Meta:
        model = Commit
        fields = ['id', 'timestamp', 'hash_id', 'message', 'url', 'author_username', 'commit_meta_data']
