from django.shortcuts import render
from celery import group
from .tasks import generate_image
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def generate_images(request):
    # getting the prompts from the POST request body
    prompts = request.data["prompts"]
    try:
        # generate_image() is the celery task which handles the image generation for a single prompt/image
        # I have executed the generate_image() task for each of the 3 prompts which creates 3 instances of the task with unique task ids
        # These 3 tasks have been grouped together, so they run in parallel to each other.
        response = group(generate_image.s(i) for i in prompts)()
        urls = response.get()
        # Sernding the response back to template API call
        return Response({"image_urls": urls}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        # Sernding the response back to template API call
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def home(request):
    return render(request, "home.html")
