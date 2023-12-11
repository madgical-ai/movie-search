import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")
VIDEO_CRIPT_GENERATE_TRANSCRIBE_FILE_URL = os.getenv("VIDEO_CRIPT_GENERATE_TRANSCRIBE_FILE_URL")



def generate_transcribe_file(video_data):

    # Set the service URL
    # generateTranscribe = "https://api.videocrypt.com/generateTranscribe"
    # generateTranscribe = "https://api.videocrypt.com/GenerateTranscript"

    # Set the input parameters
    input_params = {
        "video_id": video_data["token"],  # Assuming "token" is used for video ID
        # "video_id": "3878240_0_7982816139926658",  # test-01 video Assuming "token" is used for video ID
        "lang_setting": "3",
        "lang_option": ["en-IN", "en-US", "hi-IN"]
    }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(VIDEO_CRYPT_ACCESS_KEY.encode()).decode(),
        "secretKey": base64.b64encode(VIDEO_CRYPT_SECRET_KEY.encode()).decode()
    }

    # Make the POST request
    response = requests.post(VIDEO_CRIPT_GENERATE_TRANSCRIBE_FILE_URL, json=input_params, headers=headers)
    print("\n ---------------Generate Transcribe Response--------------------")
    print(response)
    print("---------------Generate TranscribeResponse--------------------\n")

    # Parse the JSON response
    result = response.json()

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


# generate_transcribe_file()