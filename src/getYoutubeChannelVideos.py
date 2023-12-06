# pip install --upgrade google-api-python-client

from pytube import Channel,Playlist
import googleapiclient.discovery
import urllib.error
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CLOUD_CONSOLE_API_KEY = os.getenv("GOOGLE_CLOUD_CONSOLE_API_KEY")

def getVideosUrl(channelNames):

    allVideosURL = []

    for channelName in channelNames:

        try:
            channel = Channel(f"https://www.youtube.com/c/{channelName}")

            print("----------------------------------------------------------------")
            channelName = channel.channel_name
            channelID = channel.channel_id
            print(f"Channel Name: {channelName}")
            print(f"Channel ID: {channelID}")
            print("----------------------------------------------------------------")

            # Create a YouTube API client with the provided API key
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=GOOGLE_CLOUD_CONSOLE_API_KEY)

            # Request to fetch playlists associated with the channel
            request = youtube.playlists().list(
                part="snippet",
                channelId=channelID,
                maxResults=50
            )
            response = request.execute()

            # Initialize a list to store playlist data
            playlists = []

            # Fetch all playlists by iterating through paginated results
            while request is not None:
                response = request.execute()
                playlists += response["items"]
                request = youtube.playlists().list_next(request, response)

            # Create a list to store relevant playlist information in a more structured format
            youtubePlaylistId = []
            # allVideosURL = []

            for playlist in playlists:
                youtubePlaylistId.append({
                    "PlaylistId": playlist["id"],
                    "PlaylisTitle": playlist["snippet"]["title"],
                    "ChannelId": playlist["snippet"]["channelId"]
                })
                print("----------------------------------------------------------------")
                print("PlaylisTitle - ", playlist["snippet"]["title"],"\n")
                # Create a Playlist object for the YouTube playlist
                p = Playlist(f'https://www.youtube.com/playlist?list={playlist["id"]}')

                # Iterate through the videos in the playlist
                for videoURL in p:
                    print("Videos inside playlists are - ",len(p))
                    allVideosURL.append(videoURL)
        
        except urllib.error.HTTPError as e:
            # Handle HTTP error (e.g., 404 Not Found) for this channel
            print(f"Error while processing channel '{channelName}': {e}")
            print(f"Maybe No playlist found")
            
    return allVideosURL


