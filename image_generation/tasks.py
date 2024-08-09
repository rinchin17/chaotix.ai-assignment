from time import sleep
from celery import shared_task
import base64
from django.core.files.base import ContentFile
import requests
from .models import Image

engine_id = 'stable-diffusion-xl-1024-v1-0'
# api_host = os.getenv('API_HOST', 'https://api.stability.ai')
# api_key = os.getenv("STABILITY_API_KEY")
# api_key = 'sk-axcO1LD2oIpi88SUGKjFJ5U9yfYS4Zp4QpeKFCnVMMvnRfQU' # mine
api_host = 'https://api.stability.ai'
api_key = 'sk-fDrOmEehNCHImZC0LiOgjsfGonDZsOywUaJCLsN3fqMkHJg9' #fifa

def send_request(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
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
        print('success')
        data = response.json()
        for i, image in enumerate(data["artifacts"]):
            name=prompt.replace(' ', '_') + '.png'
            image_data = ContentFile(base64.b64decode(image["base64"]), name=name)
            img = Image.objects.create(
                file_name = name,
                prompt=prompt,
                image = image_data
            )
        return img.image.url

@shared_task
def generate_image(prompt):
    print('------------ started for prompt = ' + prompt + '------------------')
    res = send_request(prompt)
    print('-------- done for prompt = '+ prompt + '-----------------')
    return res

