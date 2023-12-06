import os
import pprint
import weaviate
import pandas as pd

import streamlit as st
from dotenv import load_dotenv


from src.playlistVideosUrlHelper import getVideoUrl
from src.transcribeData import getTranscribeData
from src.dataToWeaviateHelper import pushDataToWeaviate
from src.searchDataHelper import searchData
from src.youtubePlaylistDataManager import loadPlaylistDataFromJsonFile ,checkPlaylistData
from src.deleteUnmatchEntryFromJsonFile import deleteUnmatchData
from src.azureOpenAiHelper import generateAzureOpenAiResponse
from src.llama2AnyscaleHelper import generatellama2Response

# For Image 
from src.imageSearchDataHelper import searchImages
from src.imageDataToWeaviateHelper import pushImageDataToWeaviate
from src.getFramesFromVideosHelper import video_preprocessing,create_csv_for_video_frames


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")


# Website Fonts and Title
# st.set_page_config(page_title="Video Search", page_icon="🐍", layout="wide")
st.set_page_config(page_title="Semantic Video Search", page_icon="🐍")
# st.title("Video Search Tool")
st.markdown("<h1 style='text-align: center;'>Semantic Video Search</h1>", unsafe_allow_html=True)
# Add space below the title
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


# Initialize a dictionary to store data
data = {
    "Question": [],
    "Text": [],
    "Model": [],
    "Prompt": [],
    "Model Output": [],
    "Prompt Tokens":[],
    "Completion Tokens":[],
}

jsonFilePath = "outputJSON/WeaviateClassName.json"
# Initialize an empty DataFrame
result_table = pd.DataFrame()
prompt = ""
textResult = None
imageResult = None
processDataCheck = None

playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)
client = weaviate.Client(WEAVIATE_CLUSTER_URL)
schema = client.schema.get()

deleteUnmatchData(jsonFilePath,schema)

# Initialize session_state to store state between button clicks
if "playlistDataState" not in st.session_state:
    # st.session_state.playlistDataState = []
    st.session_state.playlistDataState = loadPlaylistDataFromJsonFile(jsonFilePath)

# Add this at the beginning of your script to create a session state
if 'imageResponse' not in st.session_state:
    st.session_state.imageResponse = None


# Add a function to check if a Weaviate class already exists
def checkWeaviateClassExists(weaviateClassName):
    for class_entry in schema["classes"]:
        if weaviateClassName == class_entry["class"]:
            return True
    return False


videoSearchTab, imageSearchTab, processData= st.tabs(["Video Search", "Image Search","Process Data"])

with videoSearchTab:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    videoContainer0 = st.container()
    videoContainer1 = st.container()
    videoContainer2 = st.container()
    videoContainer3 = st.container()

    with videoContainer0:

        # # Retrieve the array of dictionaries containing playlist entries from the Streamlit session state.
        matchingEntries = []
        

        # print("playlistData  -  ",st.session_state['playlistDataState'],"\n")
        # st.session_state.matching_entries = []  # Reset the list before populating it again

        # playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)
        if processDataCheck is not None:
            playlistData = st.session_state['playlistDataState']
            for playlistEntry in playlistData:
                for classEntry in schema["classes"]:
                    if playlistEntry["converted_name"] == classEntry["class"]:
                        matchingEntries.append({
                            "playlist_name": playlistEntry["playlist_name"],
                            "converted_name": playlistEntry["converted_name"]
                        })
                        # break  # Break to avoid duplicate entries

        # print("Matching Entries:")
        # pprint.pprint(matchingEntries)



        gptModelOutput = ""
        llama2ModelOutput = ""
        ChatgptHeight = None
        llamaHeight = None

        # selectweaviateClassName = st.selectbox('Select playlist', matchingEntries)
        # Separate playlist names and converted names for display and selection
        playlistNames = [entry["playlist_name"] for entry in matchingEntries]

        # Display the select box in Streamlit UI
        selectedPlaylistName = st.selectbox('Select playlist', playlistNames)
        # print("\n",selectedPlaylistName)

        # Find the corresponding converted name based on the selected playlist name
        weaviateClassName = next((entry["converted_name"] for entry in matchingEntries if entry["playlist_name"] == selectedPlaylistName), None)
        # print("\n",weaviateClassName, " ------")

        # Input box for the question with default value
        question = st.text_input("Enter your Question")

        textReturnNumber = st.number_input("Number of Search Results", value=5, key="text_results")

        #  OpenAI model selection
        openai_model = st.selectbox('Select OpenAI Model', ["None", "gpt-3.5-turbo", "gpt-4"])

        # llama 2  model selection
        llama_model = st.selectbox('Select llama2 Model', ["None", "Llama-2-7b-chat-hf", "Llama-2-13b-chat-hf", "Llama-2-70b-chat-hf"])

        #  For button
        if st.button("Search"):

            with st.spinner("Searching Data...."):
                # height_factor = 0.45
                print("------------------------------------------------------")
                print(question)
                print(openai_model)
                print(llama_model)
                print("--------------------------------")
                textToCheck = searchData(question,textReturnNumber,weaviateClassName)

                print("---------------------------------------------")
                print(textToCheck)
                print("---------------------------------------------")

                prompt += f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textToCheck}```, focusing on text objects. Question: {question}"

                if openai_model == "None":
                    gptModelOutput = "Please Select the model to generate answer."
                    gptCompletionTokens = 0
                    gptPromptTokens = 0
                else:
                    gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
                if llama_model == "None":
                    llama2ModelOutput = "Please Select the model to generate answer."
                    llamaCompletionTokens = 0
                    llamaPromptTokens = 0
                else:
                    llama2ModelOutput,llamaCompletionTokens,llamaPromptTokens = generatellama2Response(prompt,llama_model)


                if openai_model != "None" or llama_model != "None":                    
                        result_table['Text'] = [item['text'] for item in textToCheck['data']['Get'][weaviateClassName]]
                        result_table['Video URL'] = [item['videoUrl'] for item in textToCheck['data']['Get'][weaviateClassName]]
                        result_table['Start Time'] = [item['start'] for item in textToCheck['data']['Get'][weaviateClassName]]
                        result_table['Duration'] = [item['duration'] for item in textToCheck['data']['Get'][weaviateClassName]]
                        # result_table['Prompt Used'] = [prompt] * len(textToCheck['data']['Get']['RamOne'])
                        
                        
                # ChatgptHeight = int(len(gptModelOutput) * height_factor)
                # llamaHeight = int(len(llama2ModelOutput) * height_factor)

                # Append data to the dictionary
                data["Question"].append(question)
                data["Model"].append(openai_model)
                data["Text"].append(textToCheck)
                data["Model Output"].append(gptModelOutput)
                data["Prompt"].append(prompt)
                data["Completion Tokens"].append(gptCompletionTokens)
                data["Prompt Tokens"].append(gptPromptTokens)


                # Append data to the dictionary
                data["Question"].append(question)
                data["Model"].append(llama_model)
                data["Text"].append(textToCheck)
                data["Model Output"].append(llama2ModelOutput)
                data["Prompt"].append(prompt)
                data["Completion Tokens"].append(llamaCompletionTokens)
                data["Prompt Tokens"].append(llamaPromptTokens)

                # Specify the CSV file name
                fileName = "video-search"

                # Check if the file already exists
                file_exists = os.path.exists(f"{fileName}.csv")

                # Print a message before writing data to the CSV file
                print("-----------------UI---------------")
                print(f"Data writing to {fileName}.csv file...")

                # Create a DataFrame from the data dictionary
                df = pd.DataFrame(data)

                # Append the DataFrame to the CSV file without removing existing data
                df.to_csv(f"{fileName}.csv", mode='a', header=False, index=False, encoding="utf-8")


                # Print a message after writing data to the CSV file
                print(f"Data written to {fileName}.csv file...")
                print("----------------UI----------------")

            with videoContainer1:
                if not result_table.empty:
                    # st.table(table_data)  # You can use  as well
                    st.subheader('Search Results', divider='rainbow')
                    st.dataframe(result_table,width=None,use_container_width=True)
            with videoContainer2:
                if prompt:
                    st.subheader('Prompt Used', divider='rainbow')
                    # st.code(prompt,line_numbers=True)
                    st.write(prompt)
            with videoContainer3:
                if gptModelOutput or llama2ModelOutput:
                    st.subheader('LLM Answer', divider='rainbow')
                    
                    Chatgpt, llama = st.columns(2)

                    #  For OpenAI output
                    with Chatgpt:
                        # Input box for the question with default value
                        chatGptOutput = st.text_area("OpenAI", value=gptModelOutput,height=300)

                    #  For Llama 2 output
                    with llama:
                        # Input box for the question with default value
                        # llama2Output = st.text_area("Answer of llama 2.", value=llama2ModelOutput,height=llamaHeight)
                        llama2Output = st.text_area("llama 2", value=llama2ModelOutput,height=300)


with imageSearchTab:
    # st.subheader('Search Images', divider='rainbow')
    imageContainer0 = st.container()
    imageContainer1 = st.container()

    # Initialize an empty DataFrame
    imageResponse = None  # Move the declaration outside the button block
    # Initialize an empty DataFrame
    with imageContainer0:

            # Input box for the question and number with default number value
            imageQuestion = st.text_input("Enter your Image Search Query")
            imageReturnNumber = st.number_input("Number of Search Results", value=5,key="image_results")
            print("\n-------------imageQuestion-------------------")
            print(imageQuestion)

            #  For button
            if st.button("Search Image"):
                print("\n--------------In UI imageSearchTab------------------")
                print(imageQuestion)
                print("Button Pressed")
                with st.spinner("Searching...."):
                    try:
                        imageResponse = searchImages(imageQuestion,imageReturnNumber)
                        print(imageResponse)
                        st.session_state.imageResponse = imageResponse
                        # st.write(response)
                    except Exception as e:
                        st.warning(f"An error occurred: {e}")

    with imageContainer1:
            st.subheader('Search Results', divider='rainbow')
            
            # Check if response is not None before accessing it
            # if imageResponse is not None:
            #     image_data = imageResponse["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]
            #     image_paths = [entry['imagePath'] for entry in image_data]

            #     for path in image_paths:
            #         st.image(path)
            if st.session_state.imageResponse is not None:
                image_data = st.session_state.imageResponse["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]
                # image_paths = [entry['imagePath'] for entry in image_data]

                # for path in image_paths:
                    # st.image(path)
                for entry in image_data:
                    st.image(entry['imagePath'])
                    st.write(f"Video URL: {entry['video_url_with_time']}")


with processData:

    processDataContainer = st.container() 

    # Path to the directory containing your images and Where to save downloaded videos
    imageDirectory = "images"
    videoSavePath = "Videos"
    csvFramesFile = "outputJSON/video_frames.csv"
    fps = 1  # Frames per second



    with processDataContainer:
        playlistID = st.text_input("Enter youtube playlist Id")
        # input_array = [value.strip() for value in playlistID.split(',')]
        input_array =[
        "PLNxd9fYeqXeapl8xZGkdF2aBq_jp67Wya",
        # "PLNxd9fYeqXebPQ7ZHJWYYrxCVjvPoOuJV",
        # "PLNxd9fYeqXeYEKumYSWXIGMfTX1qeyxDK",
        # "PLNxd9fYeqXeYvBUgN7PyVae0R665TJ9eB"
        ]
        print(type(input_array),"--------line no 56")
        if st.button("Process Data"):
            with st.spinner("Processing Data...."):
                newPlaylistData = checkPlaylistData(input_array,jsonFilePath)

                if newPlaylistData:
                    for entry in newPlaylistData:
                        # print(i)
                        weaviateClassName = entry['converted_name']
                        playListUrl = entry['playlist_Url']
                        playlistName = entry['playlist_name']

                        print("\n",weaviateClassName)
                        print(playListUrl)

                        # Check if the class already exists in Weaviate
                        if checkWeaviateClassExists(weaviateClassName):  # Implement this function
                            st.warning(f"The '{playlistName}' playlist already exists. Moving to the next playlist.")
                            continue
                    
                        allVideosUrl = getVideoUrl(playListUrl)
                        print("\n",allVideosUrl)
                        
                        # Initial empty list
                        allImgData = []

                        for videoUrl in allVideosUrl:
                            frames_info = video_preprocessing(videoUrl, imageDirectory,videoSavePath, fps)
                            # Add data from frames_info array to allImgData array 
                            allImgData.extend(frames_info)

                        print(f"Frames extracted and saved in '{imageDirectory}' folder.")

                        create_csv_for_video_frames(imageDirectory, csvFramesFile)
                        print(f"CSV file '{csvFramesFile}' created for storing video frames.")

                        data_entries = getTranscribeData(allVideosUrl)

                        # textResult = None
                        # imageResult = None
                        try:
                            textResult = pushDataToWeaviate(data_entries,weaviateClassName)
                            # imageResult = pushImageDataToWeaviate(allImgPaths)
                            imageResult = pushImageDataToWeaviate(allImgData)
                            
                            # result = "Data Pushed"
                            # if result is not None:
                                # st.success(f"Data Process Complete for - {playlistName} playlist.")

                            if textResult is not None and imageResult is not None:
                                st.success(f"Data Process Complete for - {playlistName} playlist.")
                                playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)
                                st.session_state.playlistDataState = playlistData  # Update the selected playlist
                                processDataCheck = "Done"
                            elif textResult is None and imageResult is not None:
                                st.warning("Image Data processed, but there was an issue with pushing Text data to Weaviate.")
                            elif textResult is not None and imageResult is None:
                                st.warning("Text data processed, but there was an issue with pushing Image data to Weaviate.")
                                playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)
                                st.session_state.playlistDataState = playlistData  # Update the selected playlist
                            else:
                                st.warning("No data processed. There was an issue with pushing both Text and Image data to Weaviate.")

                        except Exception as e:
                            st.warning(f"An error occurred: {e}")

                else:
                    st.warning("Playlist data already exists.")

            