import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

def get_language():
    getLangauge = "https://api.videocrypt.com/getLangauge"

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(VIDEO_CRYPT_ACCESS_KEY.encode()).decode(),
        "secretKey": base64.b64encode(VIDEO_CRYPT_SECRET_KEY.encode()).decode()
    }

    # Make the POST request
    response = requests.post(getLangauge,headers =headers)
    print(response)


    result = response.json()

    print(result)


def generate_transcribe_file(access_key, secret_key):
    # Set the service URL
    generateTranscribe = "https://api.videocrypt.com/generateTranscribe"

    # Set the input parameters
    input_params = {
                            "video_id":"3877918_0_9010712871672034",
                            # "lang_setting":"3",
                            # "lang_option":["en-IN","en-US","hi-IN"]
                            "lang_setting":"3",
                            "lang_option":["en-US"]
                           }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode()
    }

    # Make the POST request
    response = requests.post(generateTranscribe, json=input_params, headers=headers)

    print(response)
    # Parse the JSON response
    result = response.json()

    print(result)

# generate_transcribe_file(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY)
get_language()