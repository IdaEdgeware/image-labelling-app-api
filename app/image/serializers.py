from rest_framework import serializers

from core.models import Label, PatientInfo, Image


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for label objects"""

    class Meta:
        model = Label
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PatientInfoSerializer(serializers.ModelSerializer):
    """Serializer for patient info objects"""

    class Meta:
        model = PatientInfo
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for image objects"""
    patient_info = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=PatientInfo.objects.all()
    )
    labels = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Label.objects.all()
    )

    class Meta:
        model = Image
        fields = (
            'id', 'title', 'status', 'date', 'labels', 'patient_info'
            )
        read_only_fields = ('id',)
