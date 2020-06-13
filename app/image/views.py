from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Label, PatientInfo

from image import serializers


class BaseImageAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Base viewset for user owned image attributes"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new image"""
        serializer.save(user=self.request.user)


class LabelViewSet(BaseImageAttrViewSet):
    """Manage labels in the database"""

    queryset = Label.objects.all()
    serializer_class = serializers.LabelSerializer


class PatientInfoViewSet(BaseImageAttrViewSet):
    """Manage patient info in the database"""

    queryset = PatientInfo.objects.all()
    serializer_class = serializers.PatientInfoSerializer
