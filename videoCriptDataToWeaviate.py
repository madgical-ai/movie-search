import os
from dotenv import load_dotenv

# from src.generateVideoTranscribe import generate_transcribe_file
from src.generateVideoThumbnails import create_video_thumbnails
from src.getVideoThumbnails import get_video_thumbnails

# from src.getVideoTranscribeData import get_video_transcribe
# from src.dataToWeaviateHelper import pushDataToWeaviate
# from src.imageDataToWeaviateHelper import pushImageDataToWeaviate

# 100 words
# from src.TestgetVideoTranscribeData import get_video_transcribe


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME = os.getenv(
    "VIDEO_CRIPT_IMAGE_WEAVIATE_CLASS_NAME"
)


# for thumbnail only

video_data = {
    "id": "3914863",
    "account_id": "10002831",
    "title": "Sample_MX_Video",
    "token": "3914863_0_4706977636707355",
    "file_size": "948356.71",
    "video_length": "2432.32",
    "is_vod": "1",
    "live_status": "0",
    "file_url": "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3914863/1703829714_8836106315530689/1703829532376_514402963971579000_video_VOD.m3u8",
    "drm_status": "",
    "drm_encrypted": 0,
}

# for generating transcribe data only
# generate_transcribe_file(video_data)

# for generating thumbnails data only
# create_video_thumbnails(video_data)


imageDataArray = get_video_thumbnails(video_data)
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
