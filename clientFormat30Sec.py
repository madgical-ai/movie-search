import os
import json
import pprint
import pandas as pd
from src.getVideoDetails import get_video_details
from src.openAiHelper import generateOpenAiResponse
from src.prompt import promptV1, checkText, countNoOfOccurrences

# from src.getVideoTranscribeDataBasesOnMinutes import (
#     get_transcription_data_based_on_minutes,
# )

from src.getVideoTranscribeDataBasesOnMinutesSrtFormat import (
    get_transcription_data_based_on_minutes,
)

data = {
    "Time In": [],
    "Time Out": [],
    "Tag Category": [],
    "Tag Description": [],
    "Status": [],
}


# csvFileName = "profinity-movie-search-client-format"
csvFileName = "profinity-movie-search-result-combine"

video_data = {
    "id": "3921737",
    "account_id": "10002831",
    "title": "Sample_MX_Video",
    "token": "3921737_0_5165843200090703",
    "file_size": "948356.71",
    "video_length": "2432.32",
    "is_vod": "1",
    "live_status": "0",
    "file_url": "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3921737/1704792505_8686173245340069/1704791827614_658733090626124200_video_VOD.m3u8",
    "drm_status": "",
    "drm_encrypted": 0,
}

target_time_interval = 30
videoTextArray = get_transcription_data_based_on_minutes(
    video_data, target_time_interval
)
# pprint.pprint(videoTextArray)

openai_model = "gpt-3.5-turbo"


for dic in videoTextArray:
    print("--------------------------Open Ai--------------------------------------")
    prompt = countNoOfOccurrences

    (
        gptModelOutput,
        gptPromptTokens,
        gptCompletionTokens,
        messages,
        gptTotalCost,
        gptTotalTokens,
    ) = generateOpenAiResponse(dic["text"], prompt, openai_model)

    # Parse the JSON string
    response_json = json.loads(gptModelOutput)

    # for Cuss words
    if response_json["cuss_words_count"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Profanity")
        data["Tag Description"].append(response_json["cuss_word_names"])
        data["Status"].append("-")

    # for derogatory_remarks_targeting_society_or_religion
    elif response_json["derogatory_remarks_targeting_society_or_religion"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Derogatory_remarks")
        data["Tag Description"].append(
            response_json["derogatory_remarks_targeting_society_or_religion"]
        )
        data["Status"].append("-")

    # for derogatory_remarks_on_army
    elif response_json["derogatory_remarks_on_army"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Derogatory_remarks")
        data["Tag Description"].append(response_json["derogatory_remarks_on_army"])
        data["Status"].append("-")

    # for derogatory_remarks_on_navy
    elif response_json["derogatory_remarks_on_navy"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Derogatory_remarks")
        data["Tag Description"].append(response_json["derogatory_remarks_on_navy"])
        data["Status"].append("-")

    # for derogatory_remarks_on_air_force
    elif response_json["derogatory_remarks_on_air_force"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Derogatory_remarks")
        data["Tag Description"].append(response_json["derogatory_remarks_on_air_force"])
        data["Status"].append("-")

    # for derogatory_remarks_on_national_flag
    elif response_json["derogatory_remarks_on_national_flag"]:
        # Append data to the dictionary
        data["Time In"].append(dic["start_time"])
        data["Time Out"].append(dic["end_time"])
        data["Tag Category"].append("Derogatory_remarks")
        data["Tag Description"].append(
            response_json["derogatory_remarks_on_national_flag"]
        )
        data["Status"].append("-")


# # --------------------- Image -----------------------

import pprint
import os
from src.imageSearchDataHelper import searchImages
from src.imageDataToWeaviateHelper import pushImageDataToWeaviate
from src.getFramesFromVideosHelper import (
    video_preprocessing,
    create_csv_for_video_frames,
)
from dotenv import load_dotenv
import pandas as pd
import requests
import subprocess

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")

# Path to the directory containing your images and Where to save downloaded videos
imageDirectory = "images"
videoSavePath = "Videos"
csvFramesFile = "output/video_frames.csv"
fps = 1  # Frames per second
# new_filename = "Sample_MX_Video.mp4"
video_name = video_data["title"]
new_filename = f"{video_name}.mp4"
os.makedirs(videoSavePath, exist_ok=True)

imagesToFind = [
    "Smoking scenes",
    "Nudity",
    "Drug scene",
    "Alcohol Drinking Scene",
    "Old Lady Drinking",
]


def seconds_to_time(seconds):
    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Return the time as a string
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


for question in imagesToFind:
    number = 5

    try:
        response = searchImages(question, number)
        # print(response)
        # Extract the 'MovieImagesData' list
        movie_images_data = response["data"]["Get"]["MovieImagesData"]

        # Create a dictionary to store continuous time intervals
        continuous_time_intervals = {}

        # Iterate through the data and combine continuous time intervals
        current_start_time = None
        current_end_time = None

        totalTime = []
        # Print the time for each entry
        for image_data in movie_images_data:
            time = image_data["time"]
            # print(f"Time: {time} seconds")
            totalTime.append(time)

        # Sort the totalTime array in ascending order
        sortedTotalTime = sorted(totalTime)

        # Initialize a list to store combined time intervals
        combinedTimeIntervals = []

        # Print the sorted totalTime
        # print("Sorted Total Time:", sortedTotalTime)
        # Initialize variables to track the start and end of a continuous interval
        start_time = sortedTotalTime[0]
        end_time = sortedTotalTime[0]

        # Iterate through the sorted time values
        for time in sortedTotalTime[1:]:
            # Check if the current time is consecutive to the previous end_time
            if time == end_time + 1:
                end_time = time  # Extend the continuous interval
            else:
                # Add the current continuous interval to the result
                combinedTimeIntervals.append(
                    {"start_time": start_time, "end_time": end_time}
                )
                # Start a new continuous interval
                start_time = end_time = time

        # Add the last continuous interval to the result
        combinedTimeIntervals.append({"start_time": start_time, "end_time": end_time})

        # Print the combined time intervals
        for interval in combinedTimeIntervals:
            # print(
            #     f"Start Time: {interval['start_time']} seconds, End Time: {interval['end_time']} seconds"
            # )

            data["Time In"].append(seconds_to_time(interval["start_time"]))
            data["Time Out"].append(seconds_to_time(interval["end_time"]))
            data["Tag Category"].append(question)
            data["Tag Description"].append(question)
            data["Status"].append("-")

        totalTime = []

        # pprint.pprint(response)
        # st.write(response)
    except Exception as e:
        print(f"An error occurred: {e}")

    # for single data from weaviate based on certinaty only
    # print("--------------------------------question--------------------------------")
    # print(question)
    # for single_Data in response["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]:
    #     # print(single_Data["imagePath"])
    #     # Append data to the dictionary
    #     data["Time In"].append(seconds_to_time(single_Data["time"]))
    #     data["Time Out"].append(seconds_to_time(single_Data["time"]))
    #     data["Tag Category"].append(question)
    #     data["Tag Description"].append(question)
    #     data["Status"].append("-")

# Create a DataFrame from the updated data dictionary
df = pd.DataFrame(data)

# Sort the DataFrame by the "Time In" column
df.sort_values(by="Time In", inplace=True)


# Check if the file already exists
# file_exists2 = os.path.exists(f"output/{imageFileName}.csv")
file_exists2 = os.path.exists(os.path.join("output", f"{csvFileName}.csv"))

# Append the DataFrame to the CSV file without removing existing data
if not file_exists2:
    df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{csvFileName}.csv"),
        mode="w",
        header=True,
        index=False,
        encoding="utf-8",
    )
else:
    df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{csvFileName}.csv"),
        mode="a",
        header=False,
        index=False,
        encoding="utf-8",
    )

print(f"Data written to {csvFileName}.csv file...")
