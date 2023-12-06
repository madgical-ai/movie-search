import openai
from langchain.llms import AzureOpenAI
import os
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv

load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_TYPE = os.getenv("AZURE_OPENAI_API_TYPE")
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_USER_ID = os.getenv("AZURE_OPENAI_USER_ID")

os.environ["OPENAI_API_KEY"]=AZURE_OPENAI_API_KEY
openai.api_type  = AZURE_OPENAI_API_TYPE
openai.api_base = AZURE_OPENAI_API_BASE
openai.api_version  = AZURE_OPENAI_API_VERSION

def generateAzureOpenAiResponse(prompt,gptModelName):

    # Create the completion request using Azure OpenAI
    llm = AzureOpenAI(
        headers={
            "User-Id": AZURE_OPENAI_USER_ID
        },
        # engine="GPT4-8k",
        # model_name="gpt-4",
        # engine="GPTTURBO",
        engine="gpt-3-5",
        model_name=f"{gptModelName}",
        # temperature= 0.5   
    )
    
    with get_openai_callback() as cb:

        gptModelOutput = llm(prompt)
        print("\n-----------------------azureOpenAiHelper.py----------------------")
        print(gptModelOutput)
        gptTotalTokens = cb.total_tokens 
        gptTotalCost  = cb.total_cost
        gptSuccessfulRequests  = cb.successful_requests
        gptCompletionTokens  = cb.completion_tokens
        gptPromptTokens  = cb.prompt_tokens


    return gptModelOutput,gptCompletionTokens,gptPromptTokens