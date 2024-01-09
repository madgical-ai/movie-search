# from src.transcribeData import getTranscribeData
from dotenv import load_dotenv
import os
import pprint

import cv2
import os
import pandas as pd
from datetime import timedelta
from pytube import YouTube, Playlist


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")


def downloadYoutubeVideos(video_url, videoSavePath):
    # Ensure the save path exists
    os.makedirs(videoSavePath, exist_ok=True)

    # Create a YouTube object
    yt = YouTube(video_url)

    # Get video title and ID
    title = yt.title
    video_id = yt.video_id

    # Choose the highest resolution stream
    stream = yt.streams.get_highest_resolution()

    # Specify the new filename as the video ID with .mp4 extension
    new_filename = f"{video_id}.mp4"
    full_path = os.path.join(videoSavePath, new_filename)

    if os.path.exists(full_path):
        print(f"Video is already downloaded.")
        return new_filename
    else:
        # Download the video and rename it
        stream.download(output_path=videoSavePath, filename=new_filename)
        print(f"\nVideo downloaded and saved as '{new_filename}'.")
        return new_filename


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def video_preprocessing(video_url, output_folder, videoSavePath, fps, new_filename):
    # Download the YouTube video
    # new_filename = downloadYoutubeVideos(video_url,videoSavePath)

    # new_filename = ""

    # Extract video ID from the URL
    # video_id = video_url.split("v=")[1]
    video_id = "local001"

    # List all files in the root directory
    file_list = os.listdir(videoSavePath)
    # file_list = f"{videoSavePath}/{new_filename}"

    print("\n--------------------------------file_list--------------------------------")
    print(new_filename)
    print(file_list)
    print("--------------------------------file_list--------------------------------\n")
    print(file_list[0])
    print("--------------------------------file_list--------------------------------\n")

    # Load the video
    # cap = cv2.VideoCapture(os.path.join(videoSavePath, file_list[0]))
    cap = cv2.VideoCapture(os.path.join(videoSavePath, new_filename))

    # Create the output directory
    os.makedirs(output_folder, exist_ok=True)

    frames_info = []  # Array to hold dictionaries

    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        # Save frames at the specified frame rate
        if count % int(cap.get(cv2.CAP_PROP_FPS) / fps) == 0:
            frame_duration = count / cap.get(cv2.CAP_PROP_FPS)
            frame_duration_formatted = format_timedelta(
                timedelta(seconds=frame_duration)
            )
            frame_filename = os.path.join(
                output_folder, f"{video_id}-{frame_duration_formatted}.jpg"
            )

            # Add information to the array
            frame_info = {
                "Name": frame_filename,
                "image_path": frame_filename,
                "time": frame_duration,
                "video_url": video_url,
                "video_url_time": f"{video_url}&t={frame_duration}s",
            }

            frames_info.append(frame_info)

            cv2.imwrite(frame_filename, frame)
        count += 1

    cap.release()

    print("image saved done -- ", count)
    print("\n", frames_info)

    return frames_info


def create_csv_for_video_frames(output_folder, csv_filename):
    frame_files = [f for f in os.listdir(output_folder) if f.endswith(".jpg")]
    data = {
        "frame_filename": frame_files,
        "frame_link": [os.path.join(output_folder, f) for f in frame_files],
    }

    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)
