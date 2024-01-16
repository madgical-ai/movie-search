import os
import pprint
from dotenv import load_dotenv
from .getVideoDetails import get_video_details
import json

load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")


jsonFolder = "output"
os.makedirs(jsonFolder, exist_ok=True)


def savePlaylistDataInJsonFile(playlistData, jsonFilePath):
    # Save the list of dictionaries to a JSON file
    with open(jsonFilePath, "w") as jsonFile:
        json.dump(
            playlistData, jsonFile, indent=4
        )  # 'indent' is optional for pretty formatting


# video_data = {'id': '3879678', 'account_id': '10002831', 'title': 'test-02-22sec', 'token': '3879678_0_6537684937284509', 'file_size': '2258.61', 'video_length': '22.2222', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3879678/1702045142_5264286980555148/1702045139729_148580288932900580_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

# fromvideoDataTime = video_data["video_length"]


def get_video_thumbnails(video_data):
    video_length_float = float(video_data["video_length"])

    # Convert float to integer if needed
    max_captures_video_time = int(video_length_float)
    # Extract frame rate and calculate time intervals
    frameRateNumerator = 1
    frameRateDenominator = 1
    print(max_captures_video_time)

    videoDetails = get_video_details(video_data)
    pprint.pprint(videoDetails)

    title = videoDetails["data"]["title"]
    videoId = videoDetails["data"]["id"]
    thumbnailUrls = videoDetails["data"]["thumbnail_url"]
    original_url = videoDetails["data"]["original_url"]

    # Extracting download URLs
    download_urls = videoDetails["data"]["download_url"]
    highest_title = (
        max(item["title"] for item in download_urls) if download_urls else ""
    )
    highest_url = next(
        (item["url"] for item in download_urls if item["title"] == highest_title), ""
    )
    downloadUrl = highest_url

    time_interval = int(frameRateDenominator / frameRateNumerator)

    # Create array of dictionaries with thumbnail URLs,title,video id, video download url and frame times
    substring_to_skip = "thumbnail/"
    thumbnails_with_times = []
    updatedThumbnailUrls = []
    for url in thumbnailUrls:
        if url.count(substring_to_skip) < 2:
            updatedThumbnailUrls.append(url)

    for index in range(len(updatedThumbnailUrls)):
        for updatedUrl in updatedThumbnailUrls:
            if f"thumbnail{(index+1) * time_interval}.jpg" in updatedUrl:
                thumbnails_with_times.append(
                    {
                        "thumbnail_url": updatedUrl,
                        "frame_time": (index + 1) * time_interval,
                        "title": title,
                        "video_id": videoId,
                        "video_download_url": downloadUrl,
                        "original_url": original_url,
                    }
                )

    jsonFilePath = f"{jsonFolder}/videoCriptimageData_Array.json"

    savePlaylistDataInJsonFile(thumbnails_with_times, jsonFilePath)

    # pprint.pprint(thumbnails_with_times)
    # pprint.pprint(len(thumbnails_with_times))

    return thumbnails_with_times


# get_video_thumbnails(video_data)
