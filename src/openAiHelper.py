import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import get_openai_callback
import os
import pandas as pd
from dotenv import load_dotenv
# from prompt import promptV1, checkText, countNoOfOccurrences
load_dotenv()

# Initialize a dictionary to store data

fileName2 = "OpenAI_Response_counts"

def generateOpenAiResponse(text,prompt,openai_model):
    
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0.0, model_name=openai_model)
    messages = [
    SystemMessage(
        # content=promptV1
        # content=checkText
        content=prompt
    ),
    HumanMessage(
        content=f"Given text: '{text}'"
    ),]

    with get_openai_callback() as cb:
        # Generate a model response
        response = llm(messages)
        gptTotalTokens = cb.total_tokens 
        gptTotalCost  = cb.total_cost
        gptSuccessfulRequests  = cb.successful_requests
        gptCompletionTokens  = cb.completion_tokens
        gptPromptTokens  = cb.prompt_tokens

        # Print or use the generated response
        print("\n-----------------------OpenAiHelper.py----------------------")
        print(text)
        print(response)
        print("--------------------------------")
        print(response.content)
        print(type(response))
        print(gptCompletionTokens)
        print(gptPromptTokens)
        print(gptTotalTokens)
        print(gptTotalCost)
        print(gptSuccessfulRequests)
        print("\n-----------------------OpenAiHelper.py----------------------")

        return response.content,gptPromptTokens,gptCompletionTokens,messages,gptTotalCost,gptTotalTokens

# data2 = {
#         "Text": [],
#         "OpenAI_Response":[],
#         "Prompt":[],
#         "gptCompletionTokens":[],
#         "gptPromptTokens":[],
#         "gptTotalCost":[],
#         "gptTotalTokens":[],
#         "cuss_words_count":[],
#         "DR_Targeting_Society_or_Religion_Count":[],
#         "DR_Army_Count":[],
#         "DR_Navy_Count":[],
#         "DR_Air_Force_Count":[],
#         "DR_National_Flag_Count":[],
#         "Cuss_Word_Found":[],

#     }
# print("--------------------------------")
# response,gptPromptTokens,gptCompletionTokens,messages,gptTotalCost,gptTotalTokens = generateOpenAiResponse(text)
    
#     # Parse the JSON string
# response_json = json.loads(response)
#     # Access and print the "cuss_words_count" field
#     # cuss_words_count = response_json["cuss_words_count"]

#     data2["Text"].append(text)
#     data2["OpenAI_Response"].append(response)
#     data2["Prompt"].append(messages)
#     data2["gptCompletionTokens"].append(gptCompletionTokens)
#     data2["gptPromptTokens"].append(gptPromptTokens)
#     data2["gptTotalCost"].append(gptTotalCost)
#     data2["gptTotalTokens"].append(gptTotalTokens)
#     data2["cuss_words_count"].append(response_json["cuss_words_count"])
#     data2["DR_Targeting_Society_or_Religion_Count"].append(response_json["derogatory_remarks_targeting_society_or_religion"])
#     data2["DR_Army_Count"].append(response_json["derogatory_remarks_on_army"])
#     data2["DR_Navy_Count"].append(response_json["derogatory_remarks_on_navy"])
#     data2["DR_Air_Force_Count"].append(response_json["derogatory_remarks_on_air_force"])
#     data2["DR_National_Flag_Count"].append(response_json["derogatory_remarks_on_national_flag"])
#     data2["Cuss_Word_Found"].append(response_json["cuss_word_names"])
    

#     # Create a DataFrame from the updated data dictionary
#     df2 = pd.DataFrame(data2)

#     # Check if the file already exists
#     file_exists2 = os.path.exists(f"{fileName2}.csv")

#     # Append the DataFrame to the CSV file without removing existing data
#     if not file_exists2:
#         df2.to_csv(f"{fileName2}.csv", mode='w', header=True, index=False, encoding="utf-8")
#     else:
#         df2.to_csv(f"{fileName2}.csv", mode='a', header=False, index=False, encoding="utf-8")

#     print(f"Data written to {fileName2}.csv file...")

# print(countNoOfOccurrences)
