import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

def get_transcribe_list(access_key, secret_key, video_data):
    # Set the service URL
    listTranscribe = "https://api.videocrypt.com/listTranscribe"

    # Set the input parameters
    input_params = {
        "video_id": video_data["token"],  # Assuming "token" is used for video ID
    }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode()
    }

    # Make the POST request
    response = requests.post(listTranscribe, json=input_params, headers=headers)
    print("\n ---------------Transcribe list Response--------------------")
    print(response)
    print("---------------Transcribe list Response--------------------\n")

    # Parse the JSON response
    result = response.json()

    # Check if the request was successful
    if result.get("status"):
        print(f"\nTranscribe file generated successfully.\n")
        pprint.pprint(result)

    else:
        print(f"Error: {result['message']}")
        if result.get("error"):
            print(f"Details: {result['error']}")
