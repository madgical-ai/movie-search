import os
import re
import pprint
import shutil
import requests
from dotenv import load_dotenv
from videoDetails import get_video_details

load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")

video_data = {'id': '3877970', 'account_id': '10002831', 'title': 'test-01', 'token': '3877970_0_1783844973671850', 'file_size': '63025.42', 'video_length': '249.660952', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3877970/1701868520_9313420424950984/1701868505553_509274441213191230_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}
# video_data = {'id': '3878240', 'account_id': '10002831', 'title': 'Sample MX Video', 'token': '3878240_0_7982816139926658', 'file_size': '948356.71', 'video_length': '2432.32', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878240/1701931828_4462373797609623/1701870482943_799197347624100600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

allVideoDetails = []
videoDetails = get_video_details(VIDEO_CRYPT_ACCESS_KEY, VIDEO_CRYPT_SECRET_KEY, video_data)
# Extracting and organizing data
video_info = {
    'title': videoDetails['data']['title'],
    'duration': videoDetails['data']['duration'],
    'id': videoDetails['data']['id'],
    'file_url_hls': videoDetails['data']['file_url_hls'],
    'transcription_data': [transcript['transcript_url'] for transcript in videoDetails['data']['transcripts_data']]
}

allVideoDetails.append(video_info)
# pprint.pprint(allVideoDetails)
pprint.pprint(videoDetails)


# Create a folder named 'transcription_data' in the root directory
folder_name = 'transcription_data'
os.makedirs(folder_name, exist_ok=True) 


weaviateData = []
for videoDetails in allVideoDetails:

    # pprint.pprint(videoDetails)
    title = videoDetails['title']
    totalDuration = videoDetails['duration']
    videoId = videoDetails['id']
    fileUrlHls = videoDetails['file_url_hls']
    transcriptionData = videoDetails['transcription_data']

    # Download the file from the first URL in 'transcription_data'
    url = videoDetails['transcription_data'][0]

    # print("\n-----------------Urls----------------")
    # print(url)
    # print("-----------------Urls----------------\n")
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

        # Print the content in the terminal
        # print("\n----------content--------------------------------")
        # print(content)

        # Regular expression to match the subtitle blocks in VTT format
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d+|$)', re.DOTALL)
        
        matches = pattern.findall(content)
        
        for match in matches:
            index, start_time, end_time, text = match

            # Convert start time to seconds
            # start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
            
            # Convert start time to seconds including milliseconds
            start_time_components = start_time.split(':')
            # print("\n----------start_time_components--------------------------------")
            # print(start_time_components)
            # print("----------start_time_components--------------------------------\n")

            start_time_seconds = (
                int(start_time_components[0]) * 3600 +  # hours to seconds
                int(start_time_components[1]) * 60 +    # minutes to seconds
                float(start_time_components[2])         # seconds including milliseconds
            )
            weaviateData.append({
                'index': int(index),
                'start_time': start_time,
                'end_time': end_time,
                'text': text.strip(),
                'start_time_in_seconds': start_time_seconds,
                'title':title,
                'total_video_Duration': totalDuration,
                'video_id': videoId,
                'video_file_url_hls': fileUrlHls
            })

    else:
        print(f"Failed to download file. Status code: {response.status_code}")

print("\n----------weaviateData--------------------------------")
pprint.pprint(weaviateData)
# Delete the video folder after processing
# shutil.rmtree(folder_name)
