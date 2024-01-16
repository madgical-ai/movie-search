<h1 align="center">
    <b>Movie Search</b> 
<br>
</h1>

## Description

In this repository we are transcribing VideoCript video data into text. and then using Hugging face `intfloat/multilingual-e5-large` model to convert text into vector data and saving it into Weaviate.

To use this repository, clone this repository. You can do this with the following command.

```
git clone https://github.com/madgical-ai/movie-search.git
```

```
cd movie-search
```

[Video sample](https://drive.google.com/file/d/1SYShTqQcIdGLYgsQFaJxx0sfoKArGyY6/view?usp=sharing)

## Required Package

To install the required packages, run the following commands:

```
pip3 install -r requirements.txt
```

## Instruction

- First run the following command to start the defined services and containers

  ```
  docker-compose up -d
  ```

- Created `.env` file and then add details in the `.env file`

  Example:

  ```
  VIDEO_CRYPT_ACCESS_KEY = "<Access key from VideoCript>"
  VIDEO_CRYPT_SECRET_KEY = "<Secret key from VideoCript>"
  WEAVIATE_CLUSTER_URL = "http://localhost:2400"
  VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = VideoCriptTextData
  OPENAI_API_KEY = <OpenAi api key>
  VIDEO_CRIPT_GENERATE_TRANSCRIBE_FILE_URL = "https://api.videocrypt.com/GenerateTranscript"
  VIDEO_CRIPT_GENERATE_THUMBNAILS_URL = "https://api.videocrypt.com/createThumbnail"
  VIDEO_CRIPT_GET_VIDEO_DETAILS = "https://api.videocrypt.com/getVideoDetails"
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
- For Using Movie Search UI then you need to use the following command:

  ```
  streamlit run movieSearchUi.py
  ```

  In UI you can select question from dorpdown and the number of result you want to return default is 5 and then press on search button.

- For manually providing the video in Videos folder in root Directory and generating sheet for image and text result then you need to use the following command:
  ```
  python3 consolidatedSolution.py
  ```
- For automatically downloading the file from VideoCript Video Details url and generating sheet for image and text result then you need to use the following command:
  ```
  python3 consolidatedSolutionWithDownload.py
  ```
- For generate a sheet for time calculation, indicating the duration taken by the code from transcribing the file obtained from VideoCript to generating the results of an image search then you need to use the following command:
  ```
  python3 consolidatedSolutionWithDownloadandTime.py
  ```
