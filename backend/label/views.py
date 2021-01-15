from rest_framework import viewsets
from label.models import Label
from label.serializers import LabelSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

