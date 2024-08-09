from django.urls import path, include
from .views import generate_images

urlpatterns = [
    path('generate-image/', generate_images, name='generate_images'),
]