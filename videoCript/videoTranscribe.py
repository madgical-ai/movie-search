import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

def generate_transcribe_file(access_key, secret_key, video_data):
    # Set the service URL
    generateTranscribe = "https://api.videocrypt.com/generateTranscribe"

    # Set the input parameters
    input_params = {
        "video_id": video_data["token"],  # Assuming "token" is used for video ID
        "lang_setting": "3",
        "lang_option": ["en-IN", "en-US", "hi-IN"]
        # "lang_setting": "1",
        # "lang_option": ["en-IN"]
    }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode()
    }

    # Make the POST request
    response = requests.post(generateTranscribe, json=input_params, headers=headers)
    print("\n ---------------Generate Transcribe Response--------------------")
    print(response)
    print("---------------Generate TranscribeResponse--------------------\n")

    # Parse the JSON response
    result = response.json()

     # Parse the JSON response
    # try:
    #     result = response.json()
    # except requests.exceptions.JSONDecodeError as e:
    #     print(f"Error decoding JSON response: {e}")
    #     return

    # Check if the request was successful
    if result.get("status"):
        print(f"\nTranscribe file generated successfully.\n")
        pprint.pprint(result)

        # transcribe_id = result["data"]["transcribe_id"]
        # print(f"Transcribe file generated successfully. Transcribe ID: {transcribe_id}")
    else:
        print(f"Error: {result['message']}")
        if result.get("error"):
            print(f"Details: {result['error']}")
