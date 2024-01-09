import time
import streamlit as st
import os
import weaviate
import json
import pandas as pd
import json
from src.openAiHelper import generateOpenAiResponse
from src.prompt import promptV1, checkText, countNoOfOccurrences

from src.searchDataHelper import searchData
from sentence_transformers import SentenceTransformer, util
from PIL import Image

text_model = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")

from dotenv import load_dotenv

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
# WEAVIATE_CLASS_NAME = "PhysicsLaw"

# Website Fonts and Title
# st.set_page_config(page_title="Video Search", page_icon="🐍", layout="wide")
st.set_page_config(page_title="Movie Search", page_icon="🐍")
# st.title("Video Search Tool")
st.markdown("<h1 style='text-align: center;'>Movie Search</h1>", unsafe_allow_html=True)
# Add space below the title
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


def textToVectorSentenceTransformer(text):
    texts = [text]
    text_embeddings = text_model.encode(texts)
    return text_embeddings


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)


def searchImages(question, number):
    # vectors = convertTextToVectors(question)
    vectors = textToVectorSentenceTransformer(question)
    response = (
        client.query.get(
            f"{IMAGE_WEAVIATE_CLASS_NAME}",
            ["imagePath", "time", "video_url", "video_url_with_time"],
        )
        .with_near_vector(
            {
                "vector": vectors[0],
                # "certainty": 0.85
            }
        )
        # .with_limit(5)
        .with_limit(number)
        .with_additional(["certainty"])
        .do()
    )
    return response


# Initialize a dictionary to store data
data = {
    "Question": [],
    "Text": [],
    "Model": [],
    "Prompt": [],
    "Model Output": [],
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

container1 = st.container()
container2 = st.container()
container3 = st.container()
container4 = st.container()
ImageContainer = st.container()

# Initialize an empty DataFrame
result_table = pd.DataFrame()
prompt = ""
result = ""
gptModelOutput = ""
# Specify the CSV file name
fileName = "movie-search"

with container1:
    # if result:
    ChatgptHeight = None
    llamaHeight = None
    openai_model = "gpt-3.5-turbo"

    # Input box for the question with default value
    # question = st.text_input("Enter your Question")
    question = st.selectbox(
        "Select Question",
        [
            "Smoking scenes",
            "Cuss words",
            "Nudity",
            "Derogatory remarks on certain section of society or religion",
            "Derogatory remarks on the Army, Navy, Air Force, or national flag.",
        ],
    )
    number = st.number_input("Number of Search Results", value=5)

    #  For button
    if st.button("Search"):
        with st.spinner("Searching Data...."):
            print("------------------------------------------------------")
            print(question)
            print("------------------------------------------------------")
            if question not in ["Nudity", "Smoking scenes"]:
                textToCheck = searchData(question, number)
                print("---------------------------------------------")
                print(textToCheck)
                print("---------------------------------------------")

                if textToCheck:
                    result_table["Title"] = [
                        item["title"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    # result_table['Weaviate Distance'] = [item['_additional']["distance"] for item in textToCheck['data']['Get'][VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME]]
                    result_table["Weaviate Certainty"] = [
                        item["_additional"]["certainty"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    result_table["Text"] = [
                        item["text"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    result_table["Start Time"] = [
                        item["start_time_in_seconds"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    result_table["Video HLS Url "] = [
                        item["video_file_url_hls"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    result_table["Video Download Url"] = [
                        item["video_download_url"]
                        for item in textToCheck["data"]["Get"][
                            VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME
                        ]
                    ]
                    # result_table['Prompt Used'] = [prompt] * len(textToCheck['data']['Get']['RamOne'])

                prompt += countNoOfOccurrences

                (
                    gptModelOutput,
                    gptPromptTokens,
                    gptCompletionTokens,
                    messages,
                    gptTotalCost,
                    gptTotalTokens,
                ) = generateOpenAiResponse(
                    textToCheck, countNoOfOccurrences, openai_model
                )

                # Parse the JSON string
                response_json = json.loads(gptModelOutput)

                # Append data to the dictionary
                data["Question"].append(question)
                data["Text"].append(textToCheck)
                data["Model"].append(openai_model)
                data["Prompt"].append(messages)
                data["Model Output"].append(gptModelOutput)
                data["Prompt Tokens"].append(gptPromptTokens)
                data["Completion Tokens"].append(gptCompletionTokens)
                data["Total Cost"].append(gptTotalCost)
                data["Total Tokens"].append(gptTotalTokens)
                data["cuss_words_count"].append(response_json["cuss_words_count"])
                data["DR_Targeting_Society_or_Religion_Count"].append(
                    response_json["derogatory_remarks_targeting_society_or_religion"]
                )
                data["DR_Army_Count"].append(
                    response_json["derogatory_remarks_on_army"]
                )
                data["DR_Navy_Count"].append(
                    response_json["derogatory_remarks_on_navy"]
                )
                data["DR_Air_Force_Count"].append(
                    response_json["derogatory_remarks_on_air_force"]
                )
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
                        f"{fileName}.csv",
                        mode="w",
                        header=True,
                        index=False,
                        encoding="utf-8",
                    )
                else:
                    df2.to_csv(
                        f"{fileName}.csv",
                        mode="a",
                        header=False,
                        index=False,
                        encoding="utf-8",
                    )

                print(f"Data written to {fileName}.csv file...")

            else:
                # Print images
                # st.write("Images")
                try:
                    response = searchImages(question, number)
                    # st.write(response)
                except Exception as e:
                    st.warning(f"An error occurred: {e}")

        with ImageContainer:
            # Check if response is not None before accessing it
            if response is not None:
                st.subheader("Search Results", divider="rainbow")
                image_data = response["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]
                # image_paths = [entry['imagePath'] for entry in image_data]

                # for path in image_paths:
                # st.image(path)
                for entry in image_data:
                    st.image(entry["imagePath"])
                    st.write(entry["video_url_with_time"])
                    st.write(entry["_additional"])
                    print("\n")
                    print(question)
                    print(entry["imagePath"])
                    # st.write(f"Video URL: {entry['video_url_with_time']}")
                    print(entry["video_url_with_time"])
                    print(entry["_additional"])

        with container2:
            if not result_table.empty:
                # st.table(table_data)  # You can use  as well
                st.subheader("Search Results", divider="rainbow")
                st.dataframe(result_table, width=None, use_container_width=True)
        with container3:
            if prompt:
                st.subheader("Prompt Used", divider="rainbow")
                # st.code(prompt,line_numbers=True)
                st.write(prompt)
        with container4:
            if gptModelOutput:
                st.subheader("LLM Answer", divider="rainbow")
                chatGptOutput = st.text_area("OpenAI", value=gptModelOutput, height=300)
