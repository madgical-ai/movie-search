import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

# for creating video thumbnails 
def create_video_thumbnails(access_key, secret_key, video_data):
# def create_video_thumbnails(access_key, secret_key):
    # Set the service URL
    createThumbnail = "https://api.videocrypt.com/createThumbnail"

    # Set the input parameters
    input_params = {
        "id": video_data["token"],  # Assuming "token" is used for video ID
        # "id": "3877918_0_9010712871672034",  # Assuming "token" is used for video ID
        "Width": 1280,
        "Height": 720,
        "CodecSettings": {
            "FrameCaptureSettings": {
                "FramerateNumerator": 1, #(No. of frame)
                "FramerateDenominator": 1, #(No. of Second)
                "MaxCaptures": 1, #(maximum 5 captures)
                "Quality": 99 #(maximum 100 quality)
            }
        }
    }
                # "MaxCaptures": 5, #(maximum 5 captures)

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode()
    }

    # Make the POST request
    response = requests.post(createThumbnail, json=input_params, headers=headers)
    print("\n ---------------Thumbnails Response--------------------")
    print(response)
    print("---------------Thumbnails Response--------------------\n")

    # Parse the JSON response
    result = response.json()

    # Check if the request was successful
    if result.get("status"):
        print("\nThumbnail created successfully\n")
        pprint.pprint(result)
        # thumbnail_urls = result["data"]["thumbnail_url"]
        # for idx, url in enumerate(thumbnail_urls, 1):
        #     print(f"Thumbnail {idx}: {url}")
    else:
        print(f"Error: {result['message']}")

# create_video_thumbnails(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, video)