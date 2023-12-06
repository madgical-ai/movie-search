from src.imageDataToWeaviateHelper import pushImageDataToWeaviate
from src.getFramesFromVideosHelper import video_preprocessing,create_csv_for_video_frames
import os

# Path to the directory containing your images and Where to save downloaded videos
imageDirectory = "images"
videoSavePath = "Videos"
csvFramesFile = "outputJSON/video_frames.csv"
fps = 1  # Frames per second


# Define the video URLs
video_urls = [
    # "https://www.youtube.com/watch?v=eZ2Rt2DVGdU",
    # "https://www.youtube.com/watch?v=qeqhXvE5aPY",
    "https://www.youtube.com/watch?v=4NIoCjpqpXg",
    "https://www.youtube.com/watch?v=IY7Rkg7izwI",
    # "https://www.youtube.com/watch?v=gbhlJ_M0mYU",
    # "https://www.youtube.com/watch?v=YVurGpqGqfg",
    # "https://www.youtube.com/watch?v=wN1eQ9sfuk4",
    # "https://www.youtube.com/watch?v=ZvObUa_cxIw",
    # "https://www.youtube.com/watch?v=OMkEVX23BdM",
    # "https://www.youtube.com/watch?v=vhdRvkxIbK4",
]

for video_url in video_urls:
    video_preprocessing(video_url, imageDirectory,videoSavePath, fps)
print(f"Frames extracted and saved in '{imageDirectory}' folder.")

create_csv_for_video_frames(imageDirectory, csvFramesFile)
print(f"CSV file '{csvFramesFile}' created for storing video frames.")

allImgPaths = []

# Load and process each image in the directory
for image_file in os.listdir(imageDirectory):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        imagePath = os.path.join(imageDirectory, image_file)
        allImgPaths.append(imagePath)

data = pushImageDataToWeaviate(allImgPaths)
print(data)