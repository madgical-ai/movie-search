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


import os
import requests
import re
from pprint import pprint


def get_transcription_data_based_on_minutes(video_data):
    target_time_interval = 300
    weaviateData = []

    videoDetails = get_video_details(video_data)
    # pprint(videoDetails)

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
    pprint("--------------------------------")
    pprint(transcriptionData)

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
    pprint(url)

    response = requests.get(url)

    if response.status_code == 200:
        filename = os.path.join(folder_name, url.split("/")[-1])

        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"File downloaded and saved as '{filename}'")

        filename = os.path.join(folder_name, "srtSubtitles.srt")
        print(f"File downloaded and saved as '{filename}'")

        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        # pattern = re.compile(
        #     r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+|$)",
        #     re.DOTALL,
        # )

        # Use regular expressions to extract subtitle information
        pattern = re.compile(
            r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)\n\n",
            re.DOTALL,
        )
        matches = pattern.findall(content)

        current_chunk = ""
        current_start_time = []
        current_start_time_seconds = None
        current_end_time = None
        current_end_time_seconds = None
        totalDuration = None  # You need to set the total video duration
        final_end_Time = None

        for match in matches:
            index, start_time, end_time, text = match

            final_end_Time = end_time

            # Convert start and end time to seconds including milliseconds
            start_time_components = start_time.split(":")
            print(
                "----------------------------------float------------------------------"
            )
            print(start_time_components)
            print(type(start_time_components))
            print(start_time)
            print(type(start_time))

            start_time_seconds = (
                int(start_time_components[0]) * 3600
                + int(start_time_components[1]) * 60  # hours to seconds
                + float(  # minutes to seconds
                    start_time_components[2].replace(",", ".")
                )  # seconds including milliseconds
            )

            end_time_components = end_time.split(":")
            end_time_seconds = (
                int(end_time_components[0]) * 3600
                + int(end_time_components[1]) * 60  # hours to seconds
                + float(  # minutes to seconds
                    end_time_components[2].replace(",", ".")
                )  # seconds including milliseconds
            )

            if current_start_time_seconds is None:
                current_start_time_seconds = start_time_seconds
                current_start_time.append(start_time)

            # Check if adding the current text will exceed the target time interval
            if end_time_seconds - current_start_time_seconds <= target_time_interval:
                # Add to the current chunk
                current_chunk += text.strip() + " "
                current_end_time = end_time
                current_end_time_seconds = end_time_seconds
            else:
                # Save the current chunk and start a new one
                weaviateData.append(
                    {
                        "index": int(index),
                        "title": title,
                        "video_id": videoId,
                        # 'start_time': current_start_time,
                        "start_time": current_start_time[0].replace(",", "."),
                        "end_time": current_end_time.replace(",", "."),
                        "text": current_chunk.strip(),
                        "total_video_Duration": totalDuration,
                        "video_file_url_hls": fileUrlHls,
                        "video_download_url": downloadUrl,
                        "original_url": original_url,
                    }
                )

                # Reset for the new chunk
                current_chunk = text.strip() + " "
                current_start_time_seconds = start_time_seconds
                current_end_time_seconds = end_time_seconds
                current_start_time.clear()
                current_start_time.append(start_time)

        # Save the last chunk if it exists
        if current_chunk:
            weaviateData.append(
                {
                    "index": int(index),
                    "title": title,
                    "video_id": videoId,
                    "start_time": current_start_time[0].replace(",", "."),
                    "end_time": final_end_Time.replace(",", "."),
                    "text": current_chunk.strip(),
                    "total_video_Duration": totalDuration,
                    "video_file_url_hls": fileUrlHls,
                    "video_download_url": downloadUrl,
                    "original_url": original_url,
                }
            )

    return weaviateData


def create_chunks(filename):  # 300 seconds = 5 minutes
    target_time_interval = 600
    # Open and read the content of the file
    with open(filename, "r") as file:
        content = file.read()

    # Regular expression to match the subtitle blocks in VTT format
    pattern = re.compile(
        r"(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d+|$)",
        re.DOTALL,
    )

    matches = pattern.findall(content)

    weaviateData = []
    current_chunk = ""
    current_start_time = []
    current_start_time_seconds = None
    current_end_time = None
    current_end_time_seconds = None
    totalDuration = None  # You need to set the total video duration
    final_end_Time = None

    for match in matches:
        index, start_time, end_time, text = match

        final_end_Time = end_time

        # Convert start and end time to seconds including milliseconds
        start_time_components = start_time.split(":")
        start_time_seconds = (
            int(start_time_components[0]) * 3600
            + int(start_time_components[1]) * 60  # hours to seconds
            + float(  # minutes to seconds
                start_time_components[2]
            )  # seconds including milliseconds
        )

        end_time_components = end_time.split(":")
        end_time_seconds = (
            int(end_time_components[0]) * 3600
            + int(end_time_components[1]) * 60  # hours to seconds
            + float(  # minutes to seconds
                end_time_components[2]
            )  # seconds including milliseconds
        )

        if current_start_time_seconds is None:
            current_start_time_seconds = start_time_seconds
            current_start_time.append(start_time)

        # Check if adding the current text will exceed the target time interval
        if end_time_seconds - current_start_time_seconds <= target_time_interval:
            # Add to the current chunk
            current_chunk += text.strip() + " "
            current_end_time = end_time
            current_end_time_seconds = end_time_seconds
        else:
            # Save the current chunk and start a new one
            weaviateData.append(
                {
                    "start_time": current_start_time[0],
                    "end_time": current_end_time,
                    "start_time_seconds": current_start_time_seconds,
                    "end_time_seconds": current_end_time_seconds,
                    "text": current_chunk.strip(),
                }
            )

            # Reset for the new chunk
            current_chunk = text.strip() + " "
            current_start_time_seconds = start_time_seconds
            current_end_time_seconds = end_time_seconds
            current_start_time.clear()
            current_start_time.append(start_time)

            print(f"start_time: -----------{current_start_time}---")
            print(
                f"end_time: -------sec                               ----{current_end_time_seconds}---"
            )
            print(f"end_time: -----------{current_end_time}---")
            print(f"end_time: -------                         @@@@@----{end_time}---")

    # Save the last chunk if it exists
    print("--------------------appending this chunk------------------------")
    if current_chunk:
        weaviateData.append(
            {
                "start_time": current_start_time[0],
                "end_time": final_end_Time,
                "start_time_seconds": current_start_time_seconds,
                "end_time_seconds": current_end_time_seconds,
                "text": current_chunk.strip(),
            }
        )
        print(
            {
                "start_time": current_start_time[0],
                "end_time": final_end_Time,
                "start_time_seconds": current_start_time_seconds,
                "end_time_seconds": current_end_time_seconds,
                "text": current_chunk.strip(),
            }
        )
    print("--------------------appending this chunk------------------------")

    return weaviateData
