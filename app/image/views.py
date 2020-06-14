from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Label, PatientInfo, Image

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
        """Create a new object"""
        serializer.save(user=self.request.user)


class LabelViewSet(BaseImageAttrViewSet):
    """Manage labels in the database"""

    queryset = Label.objects.all()
    serializer_class = serializers.LabelSerializer


class PatientInfoViewSet(BaseImageAttrViewSet):
    """Manage patient info in the database"""

    queryset = PatientInfo.objects.all()
    serializer_class = serializers.PatientInfoSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """Manage images in the database"""
    serializer_class = serializers.ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """ Convert a list of  string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the images for the authenticated user"""
        labels = self.request.query_params.get('labels')
        patient_information = self.request.query_params.get('patient_info')
        queryset = self.queryset
        if labels:
            label_ids = self._params_to_ints(labels)
            queryset = queryset.filter(labels__id__in=label_ids)
        if patient_information:
            pi_ids = self._params_to_ints(patient_information)
            queryset = queryset.filter(patient_info__id__in=pi_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class """
        if self.action == 'retrieve':
            return serializers.ImageDetailSerializer
        elif self.action == 'upload_file':
            return serializers.ImageUploadSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new image"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-file')
    def upload_file(self, request, pk=None):
        """ Upload an image """
        image = self.get_object()
        serializer = self.get_serializer(
            image,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
