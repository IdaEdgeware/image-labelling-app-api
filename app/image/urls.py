from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image import views


router = DefaultRouter()
router.register('labels', views.LabelViewSet)

app_name = 'image'

urlpatterns = [
    path('', include(router.urls))
]
