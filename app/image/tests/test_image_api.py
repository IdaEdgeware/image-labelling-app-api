from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Image

from image.serializers import ImageSerializer


IMAGES_URL = reverse('image:image-list')


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
