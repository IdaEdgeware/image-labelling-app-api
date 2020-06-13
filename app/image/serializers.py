from rest_framework import serializers

from core.models import Label, PatientInfo


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
