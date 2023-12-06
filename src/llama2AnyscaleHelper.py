import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
LLAMA_OPENAI_API_BASE = os.getenv("LLAMA_OPENAI_API_BASE")
LLAMA_OPENAI_API_KEY = os.getenv("LLAMA_OPENAI_API_KEY")

def generatellama2Response(prompt,llama2_model_name):

    s = requests.Session()
    url = f"{LLAMA_OPENAI_API_BASE}/chat/completions"
    body = {
    "model": f"meta-llama/{llama2_model_name}",
    #  "messages": [{f"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Say 'test'."}]
    "messages": [{"role": "user", "content": prompt} ]
    #  "temperature": 0.7
    }
    with s.post(url, headers={"Authorization": f"Bearer {LLAMA_OPENAI_API_KEY}"}, json=body) as resp:
        print(resp.json())
        data = resp.json()

    
    # Extract the desired fields
    print("\n-----------------------llama2AnyscaleHelper.py----------------------")
    llama2ModelOutput = data['choices'][0]['message']['content']
    print(llama2ModelOutput)
    llamaCompletionTokens = data['usage']['completion_tokens']
    llamaPromptTokens = data['usage']['prompt_tokens']

    return llama2ModelOutput,llamaCompletionTokens,llamaPromptTokens