from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image import views


router = DefaultRouter()
router.register('labels', views.LabelViewSet)
router.register('patientinfo', views.PatientInfoViewSet)
router.register('images', views.ImageViewSet)

app_name = 'image'

urlpatterns = [
    path('', include(router.urls))
]
