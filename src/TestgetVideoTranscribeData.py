import os
import re
import pprint
import shutil
import requests
from dotenv import load_dotenv
from src.getVideoDetails import get_video_details

load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

# video_data = {'id': '3878939', 'account_id': '10002831', 'title': 'test-01', 'token': '3878939_0_9595157121783776', 'file_size': '63025.42', 'video_length': '249.660952', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878939/1702016671_8566789740593262/1702016649498_559005693879705600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}


def get_video_transcribe(video_data):
    weaviateData = []
    target_word_count = 100

    videoDetails = get_video_details(video_data)
    pprint.pprint(videoDetails)

    # Create a folder named 'transcription_data' in the root directory
    folder_name = "transcription_data"
    os.makedirs(folder_name, exist_ok=True)

    title = videoDetails["data"]["title"]
    totalDuration = videoDetails["data"]["duration"]
    videoId = videoDetails["data"]["id"]
    fileUrlHls = videoDetails["data"]["file_url_hls"]
    original_url = videoDetails["data"]["original_url"]
    transcriptionData = [
        transcript["transcript_url"]
        for transcript in videoDetails["data"]["transcripts_data"]
    ]
    pprint.pprint("--------------------------------")
    pprint.pprint(transcriptionData)

    # Extracting download URLs
    download_urls = videoDetails["data"]["download_url"]
    highest_title = (
        max(item["title"] for item in download_urls) if download_urls else ""
    )
    highest_url = next(
        (item["url"] for item in download_urls if item["title"] == highest_title), ""
    )
    downloadUrl = highest_url

    # Download the file from the first URL in 'transcription_data'
    url = transcriptionData[0]
    pprint.pprint(url)

    response = requests.get(url)

    if response.status_code == 200:
        # Extracting the filename from the URL
        filename = os.path.join(folder_name, url.split("/")[-1])

        # Save the file in the 'transcription_data' folder
        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"File downloaded and saved as '{filename}'")

        # Open and read the content of the file
        with open(filename, "r") as file:
            content = file.read()

        # Regular expression to match the subtitle blocks in VTT format
        pattern = re.compile(
            r"(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d+|$)",
            re.DOTALL,
        )

        matches = pattern.findall(content)

        current_chunk = ""
        current_start_time = []
        current_end_time = None

        for match in matches:
            index, start_time, end_time, text = match
            print("start time------------------------")
            print(start_time)
            current_start_time.append(start_time)

            # Convert start time to seconds including milliseconds
            start_time_components = start_time.split(":")
            start_time_seconds = (
                int(start_time_components[0]) * 3600
                + int(start_time_components[1]) * 60  # hours to seconds
                + float(  # minutes to seconds
                    start_time_components[2]
                )  # seconds including milliseconds
            )

            # Check if adding the current text will exceed the target word count
            if len(current_chunk.split()) + len(text.split()) <= target_word_count:
                # Add to the current chunk
                current_chunk += text.strip() + " "
                current_end_time = end_time
            else:
                # Save the current chunk and start a new one
                weaviateData.append(
                    {
                        "index": int(index),
                        "title": title,
                        "video_id": videoId,
                        "start_time": current_start_time[0],
                        "end_time": current_end_time,
                        "text": current_chunk.strip(),
                        "start_time_in_seconds": start_time_seconds,
                        "total_video_Duration": totalDuration,
                        "video_file_url_hls": fileUrlHls,
                        "video_download_url": downloadUrl,
                        "original_url": original_url,
                    }
                )

                # Reset for the new chunk
                current_chunk = text.strip() + " "
                current_start_time.clear()
                current_start_time.append(start_time)
                current_end_time = end_time

        # Save the last chunk if it exists
        if current_chunk:
            weaviateData.append(
                {
                    "index": int(index),
                    "title": title,
                    "video_id": videoId,
                    "start_time": current_start_time[0],
                    "end_time": current_end_time,
                    "text": current_chunk.strip(),
                    "start_time_in_seconds": start_time_seconds,
                    "total_video_Duration": totalDuration,
                    "video_file_url_hls": fileUrlHls,
                    "video_download_url": downloadUrl,
                    "original_url": original_url,
                }
            )

    pprint.pprint(weaviateData)
    for i in weaviateData:
        print("\n")
        print(i["start_time"])
        print(i["text"])
        print(i["end_time"])
        # Split the text into words
        words = i["text"].split()
        # print(words)

        # Calculate the number of words
        word_count = len(words)

        print("Number of words:", word_count)
        # print(len(i['text']))
        # print(i['start_time_in_seconds'])
    return weaviateData


print("\n----------weaviateData--------------------------------")
# get_video_transcribe(video_data)
# pprint.pprint(get_video_transcribe(video_data))

# Delete the video folder after processing
# shutil.rmtree(folder_name)
