from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Label

from image import serializers


class LabelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage labels in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Label.objects.all()
    serializer_class = serializers.LabelSerializer

    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
