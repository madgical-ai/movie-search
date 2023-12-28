import os
from dotenv import load_dotenv

from src.generateVideoTranscribe import generate_transcribe_file
from src.generateVideoThumbnails import create_video_thumbnails
from src.getVideoThumbnails import get_video_thumbnails
# from src.getVideoTranscribeData import get_video_transcribe 
from src.dataToWeaviateHelper import pushDataToWeaviate
from src.imageDataToWeaviateHelper import pushImageDataToWeaviate

# 100 words 
from src.TestgetVideoTranscribeData import get_video_transcribe 


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME")


# for thumbnail only 
# video_data = {'id': '3879678', 'account_id': '10002831', 'title': 'test-02-22sec', 'token': '3879678_0_6537684937284509', 'file_size': '2258.61', 'video_length': '22.2222', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3879678/1702045142_5264286980555148/1702045139729_148580288932900580_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}
# for transcribe only 
# video_data = {'id': '3878939', 'account_id': '10002831', 'title': 'test-01', 'token': '3878939_0_9595157121783776', 'file_size': '63025.42', 'video_length': '249.660952', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878939/1702016671_8566789740593262/1702016649498_559005693879705600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

# client Video Data 
# video_data = {'id': '3878240', 'account_id': '10002831', 'title': 'Sample MX Video', 'token': '3878240_0_7982816139926658', 'file_size': '948356.71', 'video_length': '2432.32', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3878240/1701931828_4462373797609623/1701870482943_799197347624100600_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

# video_data = {'id': '3881027', 'account_id': '10002831', 'title': 'Sample MX Video - test', 'token': '3881027_0_5504969059605334', 'file_size': '948356.71', 'video_length': '2432.32', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3881027/1702285148_2421163839989886/1702284947898_148583977353184160_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}

video_data = {'id': '3906062', 'account_id': '10002831', 'title': 'Sample MX Video', 'token': '3906062_0_6185975209995500', 'file_size': '948356.71', 'video_length': '2432.32', 'is_vod': '1', 'live_status': '0', 'file_url': 'https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3906062/1703138292_9423198083790564/1703137535370_770805509398789100_video_VOD.m3u8', 'drm_status': '', 'drm_encrypted': 0}


# for generating transcribe data only 
# generate_transcribe_file(video_data)

# for generating thumbnails data only 
create_video_thumbnails(video_data)


# imageDataArray = get_video_thumbnails(video_data)
# imageResult = pushImageDataToWeaviate(imageDataArray)
# print(len(imageDataArray))


# videoTextArray = get_video_transcribe(video_data)
# textResult = pushDataToWeaviate(videoTextArray)


# try:
#     # if imageResult is not None:
#         # print("image Data pushed to weaviate completed")
    
#     if textResult is not None:
#         print("Text Data pushed to weaviate completed")

# except Exception as e:
#     print(f"An error occurred: {e}")


















