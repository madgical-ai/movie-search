import time
import streamlit as st
import os
import weaviate
import json
import pandas as pd
from src.azureOpenAiHelper import generateAzureOpenAiResponse

from src.searchDataHelper import searchData

from dotenv import load_dotenv

load_dotenv()
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
WEAVIATE_CLASS_NAME = "PhysicsLaw"



# Website Fonts and Title
# st.set_page_config(page_title="Video Search", page_icon="🐍", layout="wide")
st.set_page_config(page_title="Movie Search", page_icon="🐍")
# st.title("Video Search Tool")
st.markdown("<h1 style='text-align: center;'>Movie Search</h1>", unsafe_allow_html=True)
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

container1 = st.container()
container2 = st.container()
container3 = st.container()
container4 = st.container()

# Initialize an empty DataFrame
result_table = pd.DataFrame()
prompt = ""

result = ""

with container1:
    # if result:
        gptModelOutput = ""
        ChatgptHeight = None
        llamaHeight = None
        openai_model = "gpt-3.5-turbo"

        # Input box for the question with default value
        # question = st.text_input("Enter your Question")
        question = st.selectbox('Select Question', ["Smoking scenes", "Cuss words", "Nudity","Derogatory remarks on certain section of society or religion","Derogatory remarks on the Army, Navy, Air Force, or national flag."])
        number = st.number_input("Number of Search Results", value=5)

        #  For button
        if st.button("Search"):

            with st.spinner("Searching Data...."):
                print("------------------------------------------------------")
                print(question)
                print("--------------------------------")
                textToCheck = searchData(question,number)

                print("---------------------------------------------")
                print(textToCheck)
                print("---------------------------------------------")

                prompt += f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textToCheck}```, focusing on text objects. Question: {question}"

                gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
                
                # Append data to the dictionary
                data["Question"].append(question)
                data["Model"].append(openai_model)
                data["Text"].append(textToCheck)
                data["Model Output"].append(gptModelOutput)
                data["Prompt"].append(prompt)
                data["Completion Tokens"].append(gptCompletionTokens)
                data["Prompt Tokens"].append(gptPromptTokens)


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
                if gptModelOutput:
                    st.subheader('LLM Answer', divider='rainbow')
                    chatGptOutput = st.text_area("OpenAI", value=gptModelOutput,height=300)
