
from rest_framework import viewsets
from repository.models import Repository
from repository.serializers import RepositorySerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

