# import weaviate
# import json

# client = weaviate.Client(url="http://13.127.55.84:2400")
# print("\nbefore delete -------")
# schema = client.schema.get()
# for i in schema["classes"]:
#     print(i["class"])

# all_objects = client.data_object.get(class_name="PhysicsLaw")
# with open(f'outputJSON/PhysicsLaw.json', 'w', encoding='utf-8') as json_file:
#         json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
    


# video_url = "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3877970/1701868520_9313420424950984/1701868505553_509274441213191230_video_VOD.m3u8"
# start_time_seconds = 220.139

# # Append the start time parameter to the video URL
# modified_video_url = f"{video_url}#t={start_time_seconds}"

# # Now you can use the modified_video_url in your Streamlit UI
# print(modified_video_url)












import os
import pprint
from dotenv import load_dotenv
from getVideoDetails import get_video_details
import json

load_dotenv()
VIDEO_CRYPT_ACCESS_KEY = os.getenv("VIDEO_CRYPT_ACCESS_KEY")
VIDEO_CRYPT_SECRET_KEY = os.getenv("VIDEO_CRYPT_SECRET_KEY")


jsonFolder = "output"
os.makedirs(jsonFolder, exist_ok=True)

def savePlaylistDataInJsonFile(playlistData, jsonFilePath):
    # Save the list of dictionaries to a JSON file
    with open(jsonFilePath, "w") as jsonFile:
        json.dump(playlistData, jsonFile, indent=4)  # 'indent' is optional for pretty formatting



def get_video_thumbnails(video_data):

    video_length_float = float(video_data['video_length'])

    # Convert float to integer if needed
    max_captures_video_time = int(video_length_float)
    # Extract frame rate and calculate time intervals
    frameRateNumerator = 1
    frameRateDenominator = 1
    print(max_captures_video_time)

    videoDetails = get_video_details(video_data)
    pprint.pprint(videoDetails)

    thumbnailUrls = videoDetails['data']['thumbnail_url']

    # Create array of dictionaries with thumbnail URLs,title,video id, video download url and frame times
    substring_to_skip = 'thumbnail/'
    thumbnails_with_times = []
    updatedThumbnailUrls = []
    for url in thumbnailUrls:
        if url.count(substring_to_skip) < 2:
            updatedThumbnailUrls.append(url)

    for index in range(len(updatedThumbnailUrls)):
        for updatedUrl in updatedThumbnailUrls:
            if f"thumbnail{(index+1) * time_interval}.jpg" in updatedUrl:
                thumbnails_with_times.append(
                    {
                        "thumbnail_url": updatedUrl, 
                        "frame_time": (index+1) * time_interval,
                        "title":title, 
                        "video_id":videoId, 
                        "video_download_url":downloadUrl,
                        "original_url": original_url
                    })

    jsonFilePath = f"{jsonFolder}/videoCriptimageData_Array.json"
    
    savePlaylistDataInJsonFile(thumbnails_with_times, jsonFilePath)
    
    pprint.pprint(thumbnails_with_times)
    pprint.pprint(len(thumbnails_with_times))

    return thumbnails_with_times

# get_video_thumbnails(video_data)







from getVideoThumbnails import get_video_thumbnails
video_data = {'id': '3878240', 'account_id': '10002831', 'title': 'Sample MX Video', 'token': '3878240_0_7982816139926658', 'file_size': '948356.71', 'video_length': '2432.32', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878240/1701931828_4462373797609623/1701870482943_799197347624100600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}
imageDataArray = get_video_thumbnails(video_data)





