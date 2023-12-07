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
    print("\n ---------------Video Details Response--------------------")
    print(response)
    print("---------------Video Details Response--------------------\n")

    # Parse the JSON response
    result = response.json()
    pprint.pprint(result)

    # # Check if the request was successful
    # if result.get("status"):
    #     print(f"\nTranscribe file generated successfully.\n")
    #     pprint.pprint(result)

    # else:
    #     print(f"Error: {result['message']}")
    #     if result.get("error"):
    #         print(f"Details: {result['error']}")

# video = {'id': '3874645', 'account_id': '10002831', 'title': 'Demo_1', 'token': '3874645_0_4249009317828403', 'file_size': '8740.66', 'video_length': '323.918367', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3874645/1701510172_2462087081146426/test/1701510160093_493486164509061060_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

# get_video_details(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video)