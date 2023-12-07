import requests
import base64
import os
import pprint
import json
from dotenv import load_dotenv
load_dotenv()
# from videoThumbnails import create_video_thumbnails
# from videoTranscribe import generate_transcribe_file
# from videoListTranscribe import get_transcribe_list
from videoDetails import get_video_details

VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")


def get_video_list(access_key, secret_key, device_type):
    # Set the service URL
    service_url = "https://api.videocrypt.com/getVideoList"

    # Set the input parameters
    input_params = {"flag": "1"}

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode(),
        "device-type": str(device_type)
    }

    # Make the POST request
    response = requests.post(service_url, data=input_params, headers=headers)
    print("\n ---------------Video List Response--------------------")
    print(response)
    print("---------------Video List Response--------------------\n")

    # Parse the JSON response
    result = response.json()

    if result.get("status"):
        for video in result["data"]["video_list"]:
            print("\n-------Videos Details ---------\n")
            print(video)
            # create_video_thumbnails(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, video)
            # generate_transcribe_file(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video)
            # get_transcribe_list(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video)
            get_video_details(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video)

    # print(response)

device_type = 1  # 1 for Android, 2 for IOS
get_video_list(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, device_type)