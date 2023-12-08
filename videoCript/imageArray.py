import os
import re
import pprint
import base64
import shutil
import requests
from dotenv import load_dotenv
from videoDetails import get_video_details
import json

def savePlaylistDataInJsonFile(playlistData, jsonFilePath):
    # Save the list of dictionaries to a JSON file
    with open(jsonFilePath, "w") as jsonFile:
        json.dump(playlistData, jsonFile, indent=4)  # 'indent' is optional for pretty formatting

def loadPlaylistDataFromJsonFile(jsonFilePath):
    print("\n---------------------youtubePlaylistDataManager.py-------------------------")
    print("Loading Playlist data from json file")
    try:
        # Try to open and read the existing JSON file
        with open(jsonFilePath, "r") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []


load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

video_data = {'id': '3879063', 'account_id': '10002831', 'title': 'test-02-22sec', 'token': '3879063_0_1589629292717089', 'file_size': '2258.61', 'video_length': '22.2222', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3879063/1702026223_2458230629338276/1702026219816_749626452548768000_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

fromvideoDataTime = video_data["video_length"]


def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

time_str = "00:04:09"
seconds = time_to_seconds(time_str)
print(f"{time_str} is equal to {seconds} seconds.")
print(f"{time_str} is equal to {fromvideoDataTime} seconds.")


def create_video_thumbnails(access_key, secret_key, video_data):
# def create_video_thumbnails(access_key, secret_key):
    # Set the service URL
    createThumbnail = "https://api.videocrypt.com/createThumbnail"
    # time = video_data['video_length']
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
        "accessKey": base64.b64encode(access_key.encode()).decode(),
        "secretKey": base64.b64encode(secret_key.encode()).decode()
    }

    # Make the POST request
    response = requests.post(createThumbnail, json=input_params, headers=headers)
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

    videoDetails = get_video_details(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_ACCESS_KEY, video_data)

    title = videoDetails['data']['title']
    videoId = videoDetails['data']['id']
    thumbnailUrls = videoDetails['data']['thumbnail_url']


    time_interval = int(frameRateDenominator / frameRateNumerator)

    print(time_interval,"    ssdsd")

    # Create array of dictionaries with thumbnail URLs and frame times
    thumbnails_with_times = [
        {"thumbnail_url": url, "frame_time": i * time_interval}
        for i, url in enumerate(thumbnailUrls)
    ]

    # Print the result
    for thumbnail_info in thumbnails_with_times:
        print(thumbnail_info)

    jsonFilePath = "outputJSON/videoCriptimageData.json"
    savePlaylistDataInJsonFile(thumbnails_with_times, jsonFilePath)


create_video_thumbnails(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, video_data)
