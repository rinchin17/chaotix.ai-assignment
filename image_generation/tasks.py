from celery import shared_task
import base64
from django.core.files.base import ContentFile
import requests
from .models import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


engine_id = "stable-diffusion-xl-1024-v1-0"
# fetching the Stability API Key and Host from the environment file
# for security reasons, the Stability API Key is sensitive and hence fetched from the .env file
api_host = os.getenv('STABILITY_API_HOST')
api_key = os.getenv('STABILITY_API_KEY')


# Sending the POST request to Stability API for the image generation
# Each prompt is passed as an argument to the send_request function
def send_request(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    else:
        data = response.json()
        artifacts = data["artifacts"]
        # creating a file name for the image
        name = prompt.replace(" ", "_") + ".png"
        # Image being converted from base64 to a File and being stored in Django
        image_data = ContentFile(base64.b64decode(artifacts[0]["base64"]), name=name)
        # Image being stored to Django project and an Image database instance is created
        img = Image.objects.create(file_name=name, prompt=prompt, image=image_data)

        # Image URL being returned to the task, so it can in turn return it to the template
        return img.image.url

@shared_task
def generate_image(prompt):
    res = send_request(prompt)
    return res
