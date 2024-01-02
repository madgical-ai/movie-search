# from src.TestgetVideoTranscribeData import get_video_transcribe
from src.getVideoTranscribeDataBasesOnMinutes import (
    get_transcription_data_based_on_minutes,
    create_chunks,
)
from src.getVideoDetails import get_video_details
import pandas as pd
import os

import json
from src.openAiHelper import generateOpenAiResponse
from src.prompt import promptV1, checkText, countNoOfOccurrences

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


import pprint

# videoTextArray = get_video_transcribe(video_data)

videoTextArray = get_transcription_data_based_on_minutes(video_data)

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

fileName = "profinity-movie-search"

for dic in videoTextArray:
    print("----------------------------------------------------------------")
    print(dic["end_time"])
    print(dic["start_time"])
    # print(dic["text"])
    print(dic["title"])
    print(dic["total_video_Duration"])
    print(dic["video_download_url"])
    print(dic["video_id"])
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
    file_exists2 = os.path.exists(f"{fileName}.csv")

    # Append the DataFrame to the CSV file without removing existing data
    if not file_exists2:
        df2.to_csv(
            f"{fileName}.csv", mode="w", header=True, index=False, encoding="utf-8"
        )
    else:
        df2.to_csv(
            f"{fileName}.csv", mode="a", header=False, index=False, encoding="utf-8"
        )

    print(f"Data written to {fileName}.csv file...")
# pprint.pprint(videoTextArray)
# response,gptPromptTokens,gptCompletionTokens,messages,gptTotalCost,gptTotalTokens = generateOpenAiResponse(text,prompt,openai_model)
# textResult = pushDataToWeaviate(videoTextArray)
