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
        "secretKey": base64.b64encode(VIDEO_CRYPT_SECRET_KEY.encode()).decode(),
    }

    # Make the POST request
    response = requests.post(
        VIDEO_CRIPT_GET_VIDEO_DETAILS, json=input_params, headers=headers
    )

    # Parse the JSON response
    result = response.json()
    # print("\n ---------------Video Details Response--------------------")
    # print(response)
    # pprint.pprint(result)
    # print("---------------Video Details Response--------------------\n")
    return result


video_data = {
    "id": "3914863",
    "account_id": "10002831",
    "title": "Sample_MX_Video",
    "token": "3914863_0_4706977636707355",
    "file_size": "948356.71",
    "video_length": "2432.32",
    "is_vod": "1",
    "live_status": "0",
    "file_url": "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3914863/1703829714_8836106315530689/1703829532376_514402963971579000_video_VOD.m3u8",
    "drm_status": "",
    "drm_encrypted": 0,
}


get_video_details(video_data)
