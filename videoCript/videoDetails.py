import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

def get_video_details(access_key, secret_key, video_data):
    # Set the service URL
    # listTranscribe = "https://api.videocrypt.com/listTranscribe"
    getVideoDetails = "https://api.videocrypt.com/getVideoDetails"

    # Set the input parameters
    input_params = {
        # "id": video_data["token"],  # Assuming "token" is used for video ID
        "id": video_data["token"],  # Assuming "token" is used for video ID
    }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(VIDEO_CRYPT_ACCESS_KEY.encode()).decode(),
        "secretKey": base64.b64encode(VIDEO_CRYPT_SECRET_KEY.encode()).decode()
    }

    # Make the POST request
    response = requests.post(getVideoDetails, json=input_params, headers=headers)

    # Parse the JSON response
    result = response.json()
    print("\n ---------------Video Details Response--------------------")
    print(response)
    pprint.pprint(result)
    print("---------------Video Details Response--------------------\n")
    return result

