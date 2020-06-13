from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PatientInfo

from image.serializers import PatientInfoSerializer

PATIENTINFO_URL = reverse('image:patientinfo-list')


class PublicPatientInfoApiTests(TestCase):
    """ Test the publicly available patient info API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving patient info"""
        res = self.client.get(PATIENTINFO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePatientInfoApiTests(TestCase):
    """ Test the private patient info API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testdomain.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_patient_info(self):
        """Test retrieving patient info"""
        PatientInfo.objects.create(user=self.user, name="Test patient1")
        PatientInfo.objects.create(user=self.user, name="Test patient2")

        res = self.client.get(PATIENTINFO_URL)

        patient_info = PatientInfo.objects.all().order_by('-name')
        serializer = PatientInfoSerializer(patient_info, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patient_info_limited_to_user(self):
        """Test that patient info returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@testdomain.com',
            'password123'
        )
        PatientInfo.objects.create(user=user2, name='Test Patient 1')
        patient_info = PatientInfo.objects.create(
            user=self.user,
            name='Test patient 2'
            )

        res = self.client.get(PATIENTINFO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], patient_info.name)

    def test_create_patient_info_successful(self):
        """ Test creating a new patient info is successful"""
        payload = {'name': 'New patient info'}
        self.client.post(PATIENTINFO_URL, payload)

        exists = PatientInfo.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_patient_info_invalid(self):
        """ Test creating a new patient info with invalid payload """
        payload = {'name': ''}
        res = self.client.post(PATIENTINFO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
