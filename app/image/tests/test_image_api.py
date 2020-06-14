from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Image, Label, PatientInfo

from image.serializers import ImageSerializer, ImageDetailSerializer


IMAGES_URL = reverse('image:image-list')


def sample_label(user, name='Diabetes'):
    """Create and return a sample label"""
    return Label.objects.create(user=user, name=name)


def sample_patient_info(user, name='Patient1'):
    """Create and return a sample patient info"""
    return PatientInfo.objects.create(user=user, name=name)


def detail_url(image_id):
    """Return image detail URL"""
    return reverse('image:image-detail', args=[image_id])


def sample_image(user, **params):
    """Create and return a sample image"""
    defaults = {
        'title': 'Sample image',
        'status': 'Sample status',
        'date': '2020-06-14',
    }
    defaults.update(params)

    return Image.objects.create(user=user, **defaults)


class PublicImageApiTests(TestCase):
    """Test unauthenticated image API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateImageApiTests(TestCase):
    """Test authenticated image API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@testdomain.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_images(self):
        """Test retrieving list of images"""
        sample_image(user=self.user)
        sample_image(user=self.user)

        res = self.client.get(IMAGES_URL)

        images = Image.objects.all().order_by('-id')
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_images_limited_to_user(self):
        """Test retrieving images for user"""
        user2 = get_user_model().objects.create_user(
            'other@testdomain.com',
            'pass'
        )
        sample_image(user=user2)
        sample_image(user=self.user)

        res = self.client.get(IMAGES_URL)

        images = Image.objects.filter(user=self.user)
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_image_detail(self):
        """Test viewing an image detail"""
        image = sample_image(user=self.user)
        image.labels.add(sample_label(user=self.user))
        image.patient_info.add(sample_patient_info(user=self.user))

        url = detail_url(image.id)
        res = self.client.get(url)

        serializer = ImageDetailSerializer(image)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_image(self):
        """ Test creating an image"""
        payload = {
            'title': 'Test image title',
            'status': 'Test status',
        }
        res = self.client.post(IMAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        image = Image.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(image, key))

    def test_create_image_with_label(self):
        """ Test creating an image with labels"""
        label1 = sample_label(user=self.user, name='Diabetes')
        label2 = sample_label(user=self.user, name='Covid-19')
        payload = {
            'title': 'Title for test image',
            'labels': [label1.id, label2.id],
            'status': 'Test status',
            'date': '2020-05-14'
        }
        res = self.client.post(IMAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        image = Image.objects.get(id=res.data['id'])
        labels = image.labels.all()
        self.assertEqual(labels.count(), 2)
        self.assertIn(label1, labels)
        self.assertIn(label2, labels)

    def test_create_image_with_patient_info(self):
        """ Test creating an image with patient info"""
        patient_info1 = sample_patient_info(user=self.user, name='Peter Jones')
        patient_info2 = sample_patient_info(user=self.user, name='Albert Str')
        payload = {
            'title': 'Title for test image',
            'patient_info': [patient_info1.id, patient_info2.id],
            'status': 'Test status',
            'date': '2020-05-14'
        }
        res = self.client.post(IMAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        image = Image.objects.get(id=res.data['id'])
        patient_info = image.patient_info.all()
        self.assertEqual(patient_info.count(), 2)
        self.assertIn(patient_info1, patient_info)
        self.assertIn(patient_info2, patient_info)