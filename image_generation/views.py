from django.shortcuts import render
from django.http import JsonResponse
from celery import group
from .tasks import generate_image
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# @csrf_exempt
@api_view(['POST'])
def generate_images(request):
    
    prompts = request.data['prompts']
    one = ['science project']
    try:
        response = group(generate_image.s(i) for i in prompts)()
        urls = response.get()
    except Exception as e:
        print(e)
    return JsonResponse({'image_urls': urls})

def home(request):
    return render(request, 'home.html')
