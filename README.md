<h1 align="center">
    <b>Semantic Video Search</b> 
<br>
</h1>

## Description
In this repository we are transcribing youtube video data into text. and then using Hugging face ```intfloat/multilingual-e5-large``` model to convert text into vector data and saving it into Weaviate.

**[Short demo usage](https://drive.google.com/file/d/1Z97No99sR7-td2DsqeH2nVNnamDOTHl_/view?usp=drive_link)**

To use this repository, clone this repository. You can do this with the following command. 
```
git clone https://github.com/madgical-ai/sementic-video-search-demo-playlist-id.git
```
```
cd sementic-video-search-demo-playlist-id
```


## Required Package 

To install the required packages, run the following commands:

```
pip3 install -r requirements.txt
```

## Instruction

[Demo Video](https://drive.google.com/file/d/1tpCEsTOqmFUsr0mnxWNpZtPjcdO1Z-Cu/view?usp=sharing)

- First run the following command to start the defined services and containers 
    ```
    docker compose up
    ```
- Second Sign in to [Google Cloud console](https://console.cloud.google.com/getting-started) 
    
    1. Select or create a project.
    
    2. In the left sidebar, go to `APIs & Services`.

    3. In the `Library` section, search for `YouTube Data API v3` and enable it.

    4. Under the same `APIs & Services` section, navigate to `Credentials`.

    5. Click `Create credentials` and choose `API Key`. Once created, copy the API key and paste it into your .env file.

- Created ```.env``` file and then add details in the ```.env file```

    Example:
    ```
    LLAMA_OPENAI_API_BASE = "<YOUR_ANYSCALE_ENDPOINT_URL>"
    LLAMA_OPENAI_API_KEY = "<YOUR_ANYSCALE_ENDPOINT_API_KEY>"
    AZURE_OPENAI_API_BASE = "<PROXY SERVER URL>"
    AZURE_OPENAI_API_TYPE  = "azure"
    AZURE_OPENAI_API_KEY = "dndskjcns"
    AZURE_OPENAI_API_VERSION  = "2023-03-15-preview"
    AZURE_OPENAI_USER_ID  = "<USER_ID proxy server>"
    WEAVIATE_CLUSTER_URL = "http://localhost:8080"
    IMAGE_WEAVIATE_CLASS_NAME = "ImagesData"
    GOOGLE_CLOUD_CONSOLE_API_KEY = "<YOUR GOOGLE CONSOLE API KEY>"
    ```

- For accessing the UI, you can run the ```combineUi.py``` file using the following command:
    ```
    streamlit run combineUi.py
    ```

## How to use the semantic video search UI

1. There are 3 tabs in Ui
    - **Video Search**
        1. In Video Search you need to select playlist from dropdown from which you want to ask questions.

            **Note:** If their is no dropdown availabe then you need to go to Process Data Tab.
        2. Enter your search query in the Enter your Question field.
        3. Select the number of search results you want to display.
        4. Select the OpenAI or llama2 model.
        5. Click the Search button.

    - **Images Search**
        1. Enter your search query in the Enter your Question field.
        2. Select the number of search results you want to display.
        3. Click the Search button.

    - **Process Data**

        1. Select input type lits its **Youtube Playlist Id** or its **YouTube Video URL**. 

        2. If you selected **Youtube Playlist Id** radio button then you need to enter one or more YouTube playlist IDs. You can separate multiple IDs with a comma.
            
            **How to get a YouTube playlist ID:**
            
            - Go to the YouTube playlist page.
            - Look at the URL in the address bar of your browser.
            - The playlist ID is the string of characters after ```list=```.
                
                For example, in the following URL:
                
                    https://www.youtube.com/playlist?list=PLmdFyQYShrjcoTLhPodQGjtZKPKIWc3Vp
                    
                The playlist ID is ```PLmdFyQYShrjcoTLhPodQGjtZKPKIWc3Vp```.
        
        3. If you selected **YouTube Video URL** radio button then you need to enter one or more YouTube video url. You can separate multiple url with a comma.

            **For example:**

                - Url = https://youtu.be/GI1tVT17gME?feature=shared
                - Playlist Name = Movies Data
