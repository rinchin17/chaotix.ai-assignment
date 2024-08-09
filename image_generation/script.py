import base64
import os
import requests

# engine_id = "stable-diffusion-v1-6"
engine_id = 'stable-diffusion-xl-1024-v1-0'
# api_host = os.getenv('API_HOST', 'https://api.stability.ai')
# api_key = os.getenv("STABILITY_API_KEY")
# api_key = 'sk-axcO1LD2oIpi88SUGKjFJ5U9yfYS4Zp4QpeKFCnVMMvnRfQU' # mine
api_host = 'https://api.stability.ai'
api_key = 'sk-fDrOmEehNCHImZC0LiOgjsfGonDZsOywUaJCLsN3fqMkHJg9' #fifa


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
                "text": "A lighthouse on a cliff"
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

data = response.json()
# print(data)

for i, image in enumerate(data["artifacts"]):
    with open(f"./images/img_{i}.png", "wb") as f:
        f.write(base64.b64decode(image["base64"]))


# import base64
# from django.core.files.base import ContentFile

# image_data = requestData['user']['image']
# format, imgstr = image_data.split(';base64,')
# print("format", format)
# ext = format.split('/')[-1]

# data = ContentFile(base64.b64decode(imgstr))  
# file_name = "'myphoto." + ext
# user.image.save(file_name, data, save=True) # image is User's model field