<h1 align="center">
    <b>Semantic Video Search</b> 
<br>
</h1>

## Description
In this repository we are transcribing VideoCript video data into text. and then using Hugging face ```intfloat/multilingual-e5-large``` model to convert text into vector data and saving it into Weaviate.

To use this repository, clone this repository. You can do this with the following command. 
```
git clone https://github.com/madgical-ai/movie-search.git
```
```
cd movie-search
```


## Required Package 

To install the required packages, run the following commands:

```
pip3 install -r requirements.txt
```

## Instruction

- Created ```.env``` file and then add details in the ```.env file```

    Example:
    ```
    AZURE_OPENAI_API_BASE = "<PROXY SERVER URL>"
    AZURE_OPENAI_API_TYPE  = "azure"
    AZURE_OPENAI_API_KEY = "dndskjcns"
    AZURE_OPENAI_API_VERSION  = "2023-03-15-preview"
    AZURE_OPENAI_USER_ID  = "<USER_ID proxy server>"
    VIDEO_CRYPT_ACCESS_KEY = "<Access key from VideoCript>"
    VIDEO_CRYPT_SECRET_KEY = "<Secret key from VideoCript>"
    ```
- After creating .env file you need to go inside videoCript folder you can do it by using the following command:
    ```
    cd videoCript
    ```
- For getting video list details from VideoCript you can use the following command:
    ```
    python3 videoList.py
    ```
- For getting video details from VideoCript you can use the following command:
    ```
    python3 videoDetails.py
    ```
- For generating transcript of the video you can use the following command:
    ```
    python3 videoTranscribe.py
    ```
- For generating thumbnails of the video you can use the following command:
    ```
    python3 videoThumbnails.py
    ```
- For generating array of dictionary for pushing it in weaviate then you need to use the following command:
    ```
    python3 app.py
    ```
- For generating thumbnails/images (1 image per second) then you need to use the following command:
    ```
    python3 generateVideoThumbnails.py
    ```
- For generating array of dictionary for pushing it in weaviate then you need to use the following command:
    ```
    python3 getVideoThumbnails.py
    ```