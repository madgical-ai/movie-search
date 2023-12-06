import os
import json
from pytube import YouTube,Playlist
from youtube_transcript_api import YouTubeTranscriptApi as yta

# Function to fetch video title and author's name
def get_video_metadata(video_url):
    yt = YouTube(video_url)
    title = yt.title
    author = yt.author
    print("\n transcribe data file     -     ",video_url )
    print("\n      -     ",title )
    print("\n      -     ",author )
    return title, author

def getTranscribeData(allVideosUrl):

    # Initialize an empty list to store the data entries
    data_entries = []

    # Define the desired length for the text (in words)
    max_words = 100

    for url in allVideosUrl:
        video_id = url.split("v=")[1]
        title, author = get_video_metadata(url)
        try:
            transcript = yta.get_transcript(video_id)
            text_accumulator = ""
            entry_start_time = None
            entry_duration = 0

            for entry in transcript:
                text_accumulator += entry["text"] + " "
                if entry_start_time is None:
                    entry_start_time = entry["start"]
                word_count = len(text_accumulator.split())
                if word_count >= max_words:
                    data_entry = {
                        "video_url": url,
                        "title": title,
                        "author": author,
                        "text": text_accumulator.strip(),
                        "start": entry_start_time,
                        "duration": entry["start"] - entry_start_time + entry["duration"],
                    }
                    data_entries.append(data_entry)
                    text_accumulator = ""
                    entry_start_time = None

            if text_accumulator:
                data_entry = {
                    "video_url": url,
                    "title": title,
                    "author": author,
                    "text": text_accumulator.strip(),
                    "start": entry_start_time,
                    "duration": entry["start"] - entry_start_time + entry["duration"],
                }
                data_entries.append(data_entry)

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    
    return data_entries

# Save data_entries to a JSON file
    # with open('outputJSON/data_entries_ProductManagement_12_Videos_Simplelearn.json', 'w') as json_file:
        # json.dump(data_entries, json_file)

    # print("Data entries saved to data_entries.json")
