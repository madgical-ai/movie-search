import time

import os
import json
import pprint
import pandas as pd
from src.getVideoDetails import get_video_details
from src.openAiHelper import generateOpenAiResponse
from src.prompt import promptV1, checkText, countNoOfOccurrences
from src.getVideoTranscribeDataBasesOnMinutes import (
    get_transcription_data_based_on_minutes,
)

calculateTime = {
    "Get Transcribe Data 5 min": [],
    "Open ai Response Time": [],
    "Total Text Time": [],
    "Download video Time": [],
    "Create image Time": [],
    "Data To weaviate time": [],
    "Generate Image csv File": [],
    "Total image Time": [],
}

startTime = time.time()
totalStartTimeText = time.time()


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

# video_data = {
#     "id": "3878939",
#     "account_id": "10002831",
#     "title": "test-01",
#     "token": "3878939_0_9595157121783776",
#     "file_size": "63025.42",
#     "video_length": "249.660952",
#     "is_vod": "1",
#     "live_status": "0",
#     "file_url": "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878939/1702016671_8566789740593262/1702016649498_559005693879705600_video_VOD.m3u8",
#     "drm_status": "",
#     "drm_encrypted": 0,
# }

videoTextArray = get_transcription_data_based_on_minutes(video_data)

end_time = time.time()
elapsed_time = end_time - startTime
print(f"Elapsed Time for converting 5 interval min : {elapsed_time:.2f} seconds")
print(f"Elapsed Time: {elapsed_time} seconds")


openai_model = "gpt-3.5-turbo"

data = {
    "Title": [],
    "Video ID": [],
    "Text": [],
    "Model": [],
    "Prompt": [],
    "OpenAI Response": [],
    "Start Time": [],
    "End Time": [],
    "Video Download URL": [],
    "Prompt Tokens": [],
    "Completion Tokens": [],
    "Total Cost": [],
    "Total Tokens": [],
    "cuss_words_count": [],
    "DR_Targeting_Society_or_Religion_Count": [],
    "DR_Army_Count": [],
    "DR_Navy_Count": [],
    "DR_Air_Force_Count": [],
    "DR_National_Flag_Count": [],
    "Cuss_Word_Found": [],
}


textFileName = "profinity-movie-search-text"

for dic in videoTextArray:
    # print("----------------------------------------------------------------")
    # print(dic["end_time"])
    # print(dic["start_time"])
    # # print(dic["text"])
    # print(dic["title"])
    # print(dic["total_video_Duration"])
    # print(dic["video_download_url"])
    # print(dic["video_id"])
    prompt = ""

    prompt += countNoOfOccurrences

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

    # Append data to the dictionary
    data["Title"].append(dic["title"])
    data["Video ID"].append(dic["video_id"])
    data["Text"].append(dic["text"])
    data["Start Time"].append(dic["start_time"])
    data["End Time"].append(dic["end_time"])
    data["Video Download URL"].append(dic["video_download_url"])
    data["OpenAI Response"].append(gptModelOutput)
    data["Model"].append(openai_model)
    data["Prompt"].append(messages)
    data["Prompt Tokens"].append(gptPromptTokens)
    data["Completion Tokens"].append(gptCompletionTokens)
    data["Total Cost"].append(gptTotalCost)
    data["Total Tokens"].append(gptTotalTokens)
    data["cuss_words_count"].append(response_json["cuss_words_count"])
    data["DR_Targeting_Society_or_Religion_Count"].append(
        response_json["derogatory_remarks_targeting_society_or_religion"]
    )
    data["DR_Army_Count"].append(response_json["derogatory_remarks_on_army"])
    data["DR_Navy_Count"].append(response_json["derogatory_remarks_on_navy"])
    data["DR_Air_Force_Count"].append(response_json["derogatory_remarks_on_air_force"])
    data["DR_National_Flag_Count"].append(
        response_json["derogatory_remarks_on_national_flag"]
    )
    data["Cuss_Word_Found"].append(response_json["cuss_word_names"])

    # Create a DataFrame from the updated data dictionary
    df2 = pd.DataFrame(data)

    # Check if the file already exists
    file_exists2 = os.path.exists(os.path.join("output", f"{textFileName}.csv"))

    # Append the DataFrame to the CSV file without removing existing data
    os.path.join("output", f"{textFileName}.csv"),
    if not file_exists2:
        df2.to_csv(
            os.path.join("output", f"{textFileName}.csv"),
            mode="w",
            header=True,
            index=False,
            encoding="utf-8",
        )
    else:
        df2.to_csv(
            os.path.join("output", f"{textFileName}.csv"),
            mode="a",
            header=False,
            index=False,
            encoding="utf-8",
        )

    print(f"Text Data written to {textFileName}.csv file...")

end_time1 = time.time()
OpenAiTimeElapsedTime = end_time1 - end_time
print(f"Elapsed Time: {OpenAiTimeElapsedTime:.2f} seconds")

totalEndTimeText = time.time()
totalElapsedTimeText = totalEndTimeText - totalStartTimeText
print(f"Elapsed Time: {totalElapsedTimeText:.2f} seconds")
# --------------------- Image -----------------------

imageStartTime = time.time()
totalStartTimeImage = time.time()

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

imageFileName = "profinity-movie-search-images"
imageData = {
    "Title": [],
    "Question": [],
    "Weaviate Certainty Score": [],
    "Images": [],
    "Start Time": [],
    "Video URL": [],
}

# Path to the directory containing your images and Where to save downloaded videos
imageDirectory = "images"
videoSavePath = "Videos"
csvFramesFile = "output/video_frames.csv"
fps = 1  # Frames per second
# new_filename = "Sample_MX_Video.mp4"
video_name = video_data["title"]
new_filename = f"{video_name}.mp4"
os.makedirs(videoSavePath, exist_ok=True)


# Define the video URLs
video_urls = [
    video_data["file_url"]
    # "https://drive.google.com/file/d/1QSocDebTBM14B9uandQqd6PAXo5PrwcF/view",
    # "https://dw3htsev2ue75.cloudfront.net/file_library/videos/original/1702045139729_148580288932900580_video_VOD.mp4",
    # "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3914863/1703829714_8836106315530689/1703829532376_514402963971579000_video_VOD.m3u8",
    # "https://dw3htsev2ue75.cloudfront.net/file_library/videos/download/3921737/1704792969_2818107061889017/1704791827614_658733090626124200_video_VOD720p30.mp4"
]

imageEndTime = None
imageDownloadTime = None
allImgData = []
for video_url in video_urls:
    # Extract file extensions
    extension = video_url.split(".")[-1]

    # Define the new filename within the 'videos' folder
    videoDownloadPath = os.path.join(videoSavePath, new_filename)

    if extension == "mp4":
        print("mp4 file")
        response = requests.get(video_url, stream=True)
        # Print the response status code
        print("Response Status Code:", response.status_code)

        # Print the headers received in the response
        print("Response Headers:", response.headers)

        if response.status_code == 200:
            with open(videoDownloadPath, "wb") as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            print("Video downloaded successfully.")
        else:
            print(f"Error: {response.status_code}")
    else:
        print("m3u8 file")
        # Construct the ffmpeg command
        ffmpeg_command = ["ffmpeg", "-i", video_url, "-c", "copy", videoDownloadPath]

        # Run the command
        try:
            subprocess.run(ffmpeg_command, check=True)
            print("Video downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    imageEndTime = time.time()
    imageDownloadTime = imageEndTime - imageStartTime
    print(f"Image download Elapsed Time: {imageDownloadTime:.2f} seconds")

    frames_info = video_preprocessing(
        video_url, imageDirectory, videoSavePath, fps, new_filename
    )
    allImgData.extend(frames_info)
print(f"Frames extracted and saved in '{imageDirectory}' folder.")

create_csv_for_video_frames(imageDirectory, csvFramesFile)
print(f"CSV file '{csvFramesFile}' created for storing video frames.")

imageEndTime2 = time.time()
imageFrameTime = imageEndTime2 - imageEndTime
print(f"Image frame creation Elapsed Time: {imageFrameTime:.2f} seconds")


data = pushImageDataToWeaviate(allImgData)
print(f"Data pusshed to weaviate completed successfully --------------- {data}")

imageEndTime3 = time.time()
imageToWeaviateTime = imageEndTime3 - imageEndTime2
print(f"Image to weaviate Elapsed Time: {imageToWeaviateTime:.2f} seconds")


imagesToFind = [
    "Smoking scenes",
    "Nudity",
]

for question in imagesToFind:
    number = 5

    try:
        response = searchImages(question, number)
        # pprint.pprint(response)
        # st.write(response)
    except Exception as e:
        print(f"An error occurred: {e}")

    # for single data from weaviate based on certinaty only
    for single_Data in response["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]:
        # Append data to the dictionary
        imageData["Title"].append(new_filename)
        imageData["Question"].append(question)
        imageData["Weaviate Certainty Score"].append(
            single_Data["_additional"]["certainty"]
        )
        imageData["Images"].append(single_Data["imagePath"])
        imageData["Start Time"].append(single_Data["time"])
        imageData["Video URL"].append(single_Data["video_url"])
        # Create a DataFrame from the updated data dictionary
        image_df = pd.DataFrame(imageData)

    # Check if the file already exists
# file_exists2 = os.path.exists(f"output/{imageFileName}.csv")
Image_file_exists = os.path.exists(os.path.join("output", f"{imageFileName}.csv"))

# Append the DataFrame to the CSV file without removing existing data
if not Image_file_exists:
    image_df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{imageFileName}.csv"),
        mode="w",
        header=True,
        index=False,
        encoding="utf-8",
    )
else:
    image_df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{imageFileName}.csv"),
        mode="a",
        header=False,
        index=False,
        encoding="utf-8",
    )

print(f"Data written to {imageFileName}.csv file...")

imageEndTime4 = time.time()
imageToCsvTime = imageEndTime4 - imageEndTime3
print(f"Image csv Elapsed Time: {imageToCsvTime:.2f} seconds")

totalEndTimeimage = time.time()
totalElapsedTimeImage = totalEndTimeimage - totalStartTimeImage
print(f"Image Total Elapsed Time: {totalElapsedTimeText:.2f} seconds")


calculateTime["Get Transcribe Data 5 min"].append(elapsed_time)
calculateTime["Open ai Response Time"].append(OpenAiTimeElapsedTime)
calculateTime["Total Text Time"].append(totalElapsedTimeText)
calculateTime["Download video Time"].append(imageDownloadTime)
calculateTime["Create image Time"].append(imageFrameTime)
calculateTime["Data To weaviate time"].append(imageToWeaviateTime)
calculateTime["Generate Image csv File"].append(imageToCsvTime)
calculateTime["Total image Time"].append(totalElapsedTimeImage)

calculateTime_df = pd.DataFrame(calculateTime)


calculateTimeCsv = "Calculate-Time"
calculateTimeCsvExists = os.path.exists(
    os.path.join("output", f"{calculateTimeCsv}.csv")
)

# Append the DataFrame to the CSV file without removing existing data
if not calculateTimeCsvExists:
    calculateTime_df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{calculateTimeCsv}.csv"),
        mode="w",
        header=True,
        index=False,
        encoding="utf-8",
    )
else:
    calculateTime_df.to_csv(
        # f"output/{imageFileName}.csv",
        os.path.join("output", f"{calculateTimeCsv}.csv"),
        mode="a",
        header=False,
        index=False,
        encoding="utf-8",
    )

print(f"Data written to {calculateTimeCsv}.csv file...")
