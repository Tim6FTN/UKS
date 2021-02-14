from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from branch.models import Branch
from branch.serializers import BranchSerializer
from repository.models import Repository


# Create your views here.
class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def list(self, request, *args, **kwargs):
        repo_id = self.request.query_params.get("id")
        branches = Branch.objects.filter(repository=repo_id)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        repository = get_object_or_404(Repository, id=self.request.query_params.get("id"))
        name = request.data['name']

        branch = Branch.objects.create(name=name, repository=repository)
        serializer = BranchSerializer(branch)
        return Response(serializer.data)