import time
import streamlit as st
import os
import weaviate
import json
import pandas as pd
from src.azureOpenAiHelper import generateAzureOpenAiResponse
from src.llama2AnyscaleHelper import generatellama2Response

from src.playlistVideosUrlHelper import getVideoUrl
from src.transcribeData import getTranscribeData
from src.dataToWeaviateHelper import pushDataToWeaviate
from src.searchDataHelper import searchData

from dotenv import load_dotenv

load_dotenv()
WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")


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

container0 = st.container()
container1 = st.container()
container2 = st.container()
container3 = st.container()
container4 = st.container()

# Initialize an empty DataFrame
result_table = pd.DataFrame()
prompt = ""

result = ""
with container0:
    playlistID = st.text_input("Enter youtube playlist Id")
    input_array = [value.strip() for value in playlistID.split(',')]
    print(type(input_array),"--------line no 55")
    if st.button("Process Data"):
        with st.spinner("Processing Data...."):
            allVideosUrl = getVideoUrl(input_array)

           # allVideosUrl = [
        #"https://www.youtube.com/watch?v=5oi5j11FkQg",
        #"https://www.youtube.com/watch?v=8YhYqN9BwB4",
        #"https://www.youtube.com/watch?v=TVAxASr0iUY",
        #"https://www.youtube.com/watch?v=Bz6vexpZItw",
         #]

            data_entries = getTranscribeData(allVideosUrl)
            try:
                result = pushDataToWeaviate(data_entries)
                if result is not None:
                    st.success("Data Process Complete.")
                # else:
                #     print("No----------")
            except Exception as e:
                # print(f"An error occurred: {e}")
                st.warning(f"An error occurred: {e}")


with container1:
    # if result:
        gptModelOutput = ""
        llama2ModelOutput = ""
        ChatgptHeight = None
        llamaHeight = None

        # Input box for the question with default value
        question = st.text_input("Enter your Question")

        number = st.number_input("Number of Search Results", value=5)

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
                textToCheck = searchData(question,number)

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
                        result_table['Text'] = [item['text'] for item in textToCheck['data']['Get'][WEAVIATE_CLASS_NAME]]
                        result_table['Video URL'] = [item['videoUrl'] for item in textToCheck['data']['Get'][WEAVIATE_CLASS_NAME]]
                        result_table['Start Time'] = [item['start'] for item in textToCheck['data']['Get'][WEAVIATE_CLASS_NAME]]
                        result_table['Duration'] = [item['duration'] for item in textToCheck['data']['Get'][WEAVIATE_CLASS_NAME]]
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
                print("--------------------------------")
                print(f"Data writing to {fileName}.csv file...")

                # Create a DataFrame from the data dictionary
                df = pd.DataFrame(data)

                # Append the DataFrame to the CSV file without removing existing data
                df.to_csv(f"{fileName}.csv", mode='a', header=False, index=False, encoding="utf-8")


                # Print a message after writing data to the CSV file
                print(f"Data written to {fileName}.csv file...")
                print("--------------------------------")

            with container2:
                if not result_table.empty:
                    # st.table(table_data)  # You can use  as well
                    st.subheader('Search Results', divider='rainbow')
                    st.dataframe(result_table,width=None,use_container_width=True)
            with container3:
                if prompt:
                    st.subheader('Prompt Used', divider='rainbow')
                    # st.code(prompt,line_numbers=True)
                    st.write(prompt)
            with container4:
                if gptModelOutput or llama2ModelOutput:
                    st.subheader('LLM Answer', divider='rainbow')
                    
                    Chatgpt, llama = st.columns(2)

                    #  For OpenAI output
                    with Chatgpt:
                        # Input box for the question with default value
                        # chatGptOutput = st.text_area("Answer of ChatGpt.", value=gptModelOutput,height=ChatgptHeight,)
                        chatGptOutput = st.text_area("OpenAI", value=gptModelOutput,height=300)

                    #  For Llama 2 output
                    with llama:
                        # Input box for the question with default value
                        # llama2Output = st.text_area("Answer of llama 2.", value=llama2ModelOutput,height=llamaHeight)
                        llama2Output = st.text_area("llama 2", value=llama2ModelOutput,height=300)
