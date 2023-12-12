import os
import weaviate
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from src.searchDataHelper import searchData
# from src.azureOpenAiHelper import generateAzureOpenAiResponse

from src.toxigenToxicWords import calculate_toxic_Words


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME")


text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
def textToVectorSentenceTransformer(text):
    texts = [text]
    text_embeddings = text_model.encode(texts)
    return text_embeddings

# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

def searchImages(question,number):
    # vectors = convertTextToVectors(question)
    vectors = textToVectorSentenceTransformer(question)
    response = (
        client.query
        .get(f"{VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME}", ["thumbnail_url",'frame_time','title','video_id','video_download_url'])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
        .do()
        )
    return(response)




# Initialize a dictionary to store data
data = {
    "Question": [],
    "Search Type": [],
    "Search Result": [],
    "Prompt": [],
    "LLM": [],

}
# Initialize a dictionary to store data
data2 = {
    "Question": [],
    "Weaviate certainty": [],
    "Text": [],
    "Score": [],

}

# question = input("Cuss words")
# question = "Can you find movies which have fuck words"
# question = "accident"
# question = "Cuss words"
question = "Find text which have cuss words"
# question = "Derogatory remarks on certain sections of society or religion"
# question = "Derogatory remarks on the Army, Navy, Air Force, or national flag"
# question = "Derogatory remarks on the Army"
# question = "Derogatory remarks on the Navy"
# question = "Derogatory remarks on the Air Force"
# question = "Derogatory remarks on the national flag"
imageResponse = None  # Move the declaration outside the button block


openai_model = "gpt-3.5-turbo"


# if question == "Detect Smoking scenes":
#     number = 5
#     imageResponse = searchImages(question,number)
#     imageResponse = imageResponse['data']['Get'][VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME]
#     searchType = "image search"
#     # Append data to the dictionary
#     data["Question"].append(question)
#     data["Search Type"].append(searchType)
#     data["Search Result"].append(imageResponse)
      
# if question == "Nudity":
#     number = 5
#     imageResponse = searchImages(question,number)
#     imageResponse = imageResponse['data']['Get'][VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME]
#     searchType = "image search"
#     # Append data to the dictionary
#     data["Question"].append(question)
#     data["Search Type"].append(searchType)
#     data["Search Result"].append(imageResponse)
      
# elif question == "Cuss words":
#     number = 10
#     textResponse = searchData(question,number)
#     textResponse = textResponse['data']['Get'][VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME]
#     # print(textResponse)
#     searchType = "video search"
#     # Append data to the dictionary
#     data["Question"].append(question)
#     data["Search Type"].append(searchType)
#     data["Search Result"].append(textResponse)
    
#     prompt = f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textResponse}```, focusing on text objects. Question: {question}"
#     gptModelOutput = ''
#     # gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
#     data["Prompt"].append(prompt)
#     data["LLM"].append(gptModelOutput)
      
# elif question == "Derogatory remarks on certain sections of society or religion":
#     number = 10
#     textResponse = searchData(question,number)
#     textResponse = textResponse['data']['Get'][VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME]
#     searchType = "video search"
#     # print(textResponse)
#     # Append data to the dictionary
#     data["Question"].append(question)
#     data["Search Type"].append(searchType)
#     data["Search Result"].append(textResponse)
#     prompt = f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textResponse}```, focusing on text objects. Question: {question}"
#     # gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
#     gptModelOutput = ''
#     data["Prompt"].append(prompt)
#     data["LLM"].append(gptModelOutput)
      
# elif question == "Derogatory remarks on the Army, Navy, Air Force, or national flag":
#     number = 10
#     textResponse = searchData(question,number)
#     textResponse = textResponse['data']['Get'][VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME]
#     searchType = "video search"
#     # print(textResponse)
#     # Append data to the dictionary
#     data["Question"].append(question)
#     data["Search Type"].append(searchType)
#     data["Search Result"].append(textResponse)
#     prompt = f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textResponse}```, focusing on text objects. Question: {question}"
#     # gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
#     gptModelOutput = ''
#     data["Prompt"].append(prompt)
#     data["LLM"].append(gptModelOutput)


if question is None:
    print("Please enter question")
else:
    print("\nElse part")
    number = 10
    textResponse = searchData(question,number)
    textResponse = textResponse['data']['Get'][VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME]
    # print(textResponse)
    searchType = "video search"
    # Append data to the dictionary
    data["Question"].append(question)
    data["Search Type"].append(searchType)
    data["Search Result"].append(textResponse)
    prompt = f"You are a grade 10 teacher and your job is to give a answer to the question asked by student according to the given text. Given data ``` {textResponse}```, focusing on text objects. Question: {question}"
    gptModelOutput = ''
    # gptModelOutput,gptCompletionTokens,gptPromptTokens = generateAzureOpenAiResponse(prompt,openai_model)
    data["Prompt"].append(prompt)
    data["LLM"].append(gptModelOutput)



print("\n-----------------Text Response------------------------")
for i in textResponse:
    print(i["_additional"])
    print(i["text"])

    errorRate = calculate_toxic_Words(i['text'])

    print(f"\nProbability the input text was toxic according to ToxDectRoBERTa: {errorRate:.3g}%")
    print(errorRate)

    print('\n')


    data2["Question"].append(question)
    data2["Text"].append(i["text"])
    data2["Score"].append(errorRate)
    data2["Weaviate certainty"].append(i["_additional"]['certainty'])




print("-----------------Text Response------------------------\n")
# Specify the CSV file name
fileName = "Search"
fileName2 = "ToxicWordsResponse"

            # Check if the file already exists
file_exists = os.path.exists(f"{fileName}.csv")
file_exists2 = os.path.exists(f"{fileName2}.csv")

            # Print a message before writing data to the CSV file
print("--------------------------------")
print(f"Data writing to {fileName}.csv file...")
# print(f"Data writing to {fileName2}.csv file...")

            # Create a DataFrame from the data dictionary
df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)

            # Append the DataFrame to the CSV file without removing existing data
df.to_csv(f"{fileName}.csv", mode='a', header=False, index=False, encoding="utf-8")
# df.to_csv(f"{fileName}.csv", mode='a', header=True, index=False, encoding="utf-8")
df2.to_csv(f"{fileName2}.csv", mode='a', header=False, index=False, encoding="utf-8")
# df2.to_csv(f"{fileName2}.csv", mode='a', header=True, index=False, encoding="utf-8")


            # Print a message after writing data to the CSV file
print(f"Data written to {fileName2}.csv file...")
print("--------------------------------")

# if imageResponse is not None:
#             image_data = imageResponse["data"]["Get"][VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME]
#             image_paths = [entry['imagePath'] for entry in image_data]
           