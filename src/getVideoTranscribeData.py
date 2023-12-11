import os
import re
import pprint
import shutil
import requests
from dotenv import load_dotenv
from getVideoDetails import get_video_details

load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

video_data = {'id': '3878939', 'account_id': '10002831', 'title': 'test-01', 'token': '3878939_0_9595157121783776', 'file_size': '63025.42', 'video_length': '249.660952', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878939/1702016671_8566789740593262/1702016649498_559005693879705600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

def get_video_transcribe(video_data):

    weaviateData = []

    videoDetails = get_video_details(video_data)
    pprint.pprint(videoDetails)

    # Create a folder named 'transcription_data' in the root directory
    folder_name = 'transcription_data'
    os.makedirs(folder_name, exist_ok=True) 

    title = videoDetails['data']['title']
    totalDuration = videoDetails['data']['duration']
    videoId = videoDetails['data']['id']
    fileUrlHls = videoDetails['data']['file_url_hls']
    original_url = videoDetails['data']['original_url']
    transcriptionData = [transcript['transcript_url'] for transcript in videoDetails['data']['transcripts_data']]
    pprint.pprint("--------------------------------")
    pprint.pprint(transcriptionData)

    # Extracting download URLs
    download_urls = videoDetails['data']['download_url']
    highest_title = max(item['title'] for item in download_urls) if download_urls else ''
    highest_url = next((item['url'] for item in download_urls if item['title'] ==highest_title), '')
    downloadUrl = highest_url

    # Download the file from the first URL in 'transcription_data'
    url = transcriptionData[0]
    pprint.pprint(url)

    response = requests.get(url)

    if response.status_code == 200:
        # Extracting the filename from the URL
        filename = os.path.join(folder_name, url.split('/')[-1])

        # Save the file in the 'transcription_data' folder
        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded and saved as '{filename}'")


        # Open and read the content of the file
        with open(filename, 'r') as file:
            content = file.read()


        # Regular expression to match the subtitle blocks in VTT format
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d+|$)', re.DOTALL)
        
        matches = pattern.findall(content)

        for match in matches:
            index, start_time, end_time, text = match

            # Convert start time to seconds including milliseconds
            start_time_components = start_time.split(':')

            start_time_seconds = (
                int(start_time_components[0]) * 3600 +  # hours to seconds
                int(start_time_components[1]) * 60 +    # minutes to seconds
                float(start_time_components[2])         # seconds including milliseconds
            )


            weaviateData.append({
                'index': int(index),
                'title':title,
                'video_id': videoId,
                'start_time': start_time,
                'end_time': end_time,
                'text': text.strip(),
                'start_time_in_seconds': start_time_seconds,
                'total_video_Duration': totalDuration,
                'video_file_url_hls': fileUrlHls,
                'video_download_url': downloadUrl,
                "original_url": original_url
            })

    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    

    pprint.pprint(weaviateData)
    for i in weaviateData:
        print(i['text'])
        print(len(i['text']))
        print(i['start_time'])
        print(i['start_time_in_seconds'])
    
    return weaviateData

print("\n----------weaviateData--------------------------------")
get_video_transcribe(video_data)
# pprint.pprint(get_video_transcribe(video_data))

# Delete the video folder after processing
# shutil.rmtree(folder_name)
