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
