import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")
VIDEO_CRIPT_GET_VIDEO_DETAILS = os.getenv("VIDEO_CRIPT_GET_VIDEO_DETAILS")

def get_video_details(video_data):
    # Set the service URL
    # listTranscribe = "https://api.videocrypt.com/listTranscribe"
    # VIDEO_CRIPT_GET_VIDEO_DETAILS = 

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
    response = requests.post(VIDEO_CRIPT_GET_VIDEO_DETAILS, json=input_params, headers=headers)

    # Parse the JSON response
    result = response.json()
    print("\n ---------------Video Details Response--------------------")
    print(response)
    pprint.pprint(result)
    print("---------------Video Details Response--------------------\n")
    return result

