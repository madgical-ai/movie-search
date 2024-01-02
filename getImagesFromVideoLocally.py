from src.imageDataToWeaviateHelper import pushImageDataToWeaviate
from src.getFramesFromVideosHelper import video_preprocessing,create_csv_for_video_frames
import pprint
import os


# Path to the directory containing your images and Where to save downloaded videos
imageDirectory = "images"
videoSavePath = "Videos"
csvFramesFile = "output/video_frames.csv"
fps = 1  # Frames per second
new_filename = "Sample_MX_Video.mp4"


# Define the video URLs
video_urls = [
    "https://drive.google.com/file/d/1QSocDebTBM14B9uandQqd6PAXo5PrwcF/view",  #first law
    # "https://www.youtube.com/watch?v=8YhYqN9BwB4",  #second law
    # "https://www.youtube.com/watch?v=TVAxASr0iUY", #third law
    # "https://www.youtube.com/watch?v=Bz6vexpZItw", #FIRST LAW OF THERMODYNAMICS
    # "https://www.youtube.com/watch?v=Kw51KiZhm0I", #gravity
    # "https://www.youtube.com/watch?v=IJWEtCRWGvI",  #what is force

    
    ]


allImgData = []
for video_url in video_urls:
    frames_info = video_preprocessing(video_url, imageDirectory,videoSavePath, fps, new_filename)
    allImgData.extend(frames_info)
print(f"Frames extracted and saved in '{imageDirectory}' folder.")

create_csv_for_video_frames(imageDirectory, csvFramesFile)
print(f"CSV file '{csvFramesFile}' created for storing video frames.")


data = pushImageDataToWeaviate(allImgData)

print("\n------------------------Image Data --------------------------------")
# pprint.pprint(allImgData)
print(allImgData)
print(data)
print("------------------------Image Data --------------------------------\n")