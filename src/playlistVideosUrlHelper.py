from pytube import Playlist
import urllib.error
# from youtubePlaylistDataManager import checkPlaylistData

# def getVideoUrl(playlistId):
def getVideoUrl(playListUrl):
    allVideosURL = []   
    try:
        # for playlist in playlistId:
            # p = Playlist(f'https://www.youtube.com/playlist?list={playlist}')
            p = Playlist(playListUrl)
            # Iterate through the videos in the playlist
            for videoURL in p:
                allVideosURL.append(videoURL)
            print("\n In playlistVideosUrlHelper.py file ")
            print("Videos inside playlists are - ",len(p))
        
    except urllib.error.HTTPError as e:
            # Handle HTTP error (e.g., 404 Not Found) for this channel
            # print(f"Error while processing channel '{playlist}': {e}")
            print(f"Error while processing playlist - '{playListUrl}': {e}")
            print(f"Maybe No playlist found")

    return allVideosURL



# https://www.youtube.com/playlist?list=PLmdFyQYShrjcoTLhPodQGjtZKPKIWc3Vp

# playlistId = ["PLmdFyQYShrjcoTLhPodQGjtZKPKIWc3Vp"]
# a = pushData(playlistId)
# print(a)
            
    # PLWMr6-kiy-EwvINzrvp3H7p9wuGCcixQs