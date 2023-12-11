import os
import pprint
import base64
import requests
from dotenv import load_dotenv


load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")
VIDEO_CRIPT_GENERATE_THUMBNAILS_URL = os.getenv("VIDEO_CRIPT_GENERATE_THUMBNAILS_URL")

def create_video_thumbnails(video_data):

    # Set the service URL
    # VIDEO_CRIPT_GENERATE_THUMBNAILS_URL = 

    # Convert video_length from string to float
    video_length_float = float(video_data['video_length'])

    # Convert float to integer if needed
    max_captures_video_time = int(video_length_float)
    max_captures = 5
    # Extract frame rate and calculate time intervals
    frameRateNumerator = 1
    frameRateDenominator = 1
    print(max_captures_video_time)
    print(max_captures)
    
    # Set the input parameters
    input_params = {
        "id": video_data["token"],  # Assuming "token" is used for video ID
        # "id": "3877918_0_9010712871672034",  # Assuming "token" is used for video ID
        "Width": 1280,
        "Height": 720,
        "CodecSettings": {
            "FrameCaptureSettings": {
                "FramerateNumerator": frameRateNumerator, #(No. of frame)
                "FramerateDenominator": frameRateDenominator, #(No. of Second)
                "MaxCaptures": max_captures_video_time, #(maximum 5 captures)
                "Quality": 99 #(maximum 100 quality)
            }
        }
    }

    # Set the header parameters
    headers = {
        "accessKey": base64.b64encode(VIDEO_CRYPT_ACCESS_KEY.encode()).decode(),
        "secretKey": base64.b64encode(VIDEO_CRYPT_SECRET_KEY.encode()).decode()
    }

    # Make the POST request
    response = requests.post(VIDEO_CRIPT_GENERATE_THUMBNAILS_URL, json=input_params, headers=headers)
    print("\n ---------------Thumbnails Response--------------------")
    print(response)

    
    # Parse the JSON response
    result = response.json()

    # Check if the request was successful
    if result.get("status"):
        print("\nThumbnail created successfully\n")
        pprint.pprint(result)
    else:
        print(f"Error: {result['message']}")
    print("---------------Thumbnails Response--------------------\n")

# create_video_thumbnails(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, video_data)