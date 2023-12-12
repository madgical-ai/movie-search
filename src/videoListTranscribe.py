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
    # listTranscribe = "https://api.videocrypt.com/listTranscribe"
    listTranscribe = "https://api.videocrypt.com/listTranscribe"

    # Set the input parameters
    input_params = {
        "video_id": video_data["token"],  # Assuming "token" is used for video ID
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

video = {'id': '3874645', 'account_id': '10002831', 'title': 'Demo_1', 'token': '3874645_0_4249009317828403', 'file_size': '8740.66', 'video_length': '323.918367', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3874645/1701510172_2462087081146426/test/1701510160093_493486164509061060_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

get_transcribe_list(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video)