from django.shortcuts import render
from rest_framework import viewsets
from commit.models import Commit
from commit.serializers import CommitSerializer
from branch.models import Branch

from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Create your views here.
class CommitViewSet(viewsets.ModelViewSet):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

    def list(self, request, *args, **kwargs):
        branch_id = self.request.query_params.get("id")
        commits = Commit.objects.filter(branch=branch_id)
        serializer = CommitSerializer(commits, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        branch = get_object_or_404(Branch, id=self.request.query_params.get("id"))
        commit_hash = request.data['hash']
        message = request.data['message']

        commit = Commit.objects.create(branch=branch, hash=commit_hash, message= message)
        serializer = CommitSerializer(commit)
        return Response(serializer.data)
        
