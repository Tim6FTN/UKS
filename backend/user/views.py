from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def profile(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
