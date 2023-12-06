import json
from pytube import Playlist

def savePlaylistDataInJsonFile(playlistData, jsonFilePath):
    # Save the list of dictionaries to a JSON file
    with open(jsonFilePath, "w") as jsonFile:
        json.dump(playlistData, jsonFile, indent=4)  # 'indent' is optional for pretty formatting

def loadPlaylistDataFromJsonFile(jsonFilePath):
    print("\n---------------------youtubePlaylistDataManager.py-------------------------")
    print("Loading Playlist data from json file")
    try:
        # Try to open and read the existing JSON file
        with open(jsonFilePath, "r") as jsonFile:
            return json.load(jsonFile)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

def checkPlaylistData(videoUrlList, jsonFilePath):
    
    # Load existing playlist data from the JSON file which have orignal playlist name with channel name and weaviate class name 
    playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)

    newDataAddedToJsonFile = False  # Flag to track whether new data is added
    newData = []

    for playlistId in videoUrlList:
        # playlistUrl = '
        playlist = Playlist(f'https://www.youtube.com/playlist?list={playlistId}')
        orignalPlaylistName = playlist.title
        convertedPlaylistNameForWeaviate = orignalPlaylistName.replace(' ', '').replace('|', '_')

        print(f"\nChecking data for Playlist Name: {orignalPlaylistName}")

        # Check if the playlist name already exists in the data
        existingPlaylistData = next((p for p in playlistData if p["playlist_name"] == orignalPlaylistName), None)

        if existingPlaylistData:
            print("\nPlaylist data already exists.")
        else:
            print(f"\nAdding new data for Playlist Name: {orignalPlaylistName}")
            # Add new data to the list of dictionaries
            playlistData.append({
                "playlist_name": orignalPlaylistName, 
                "converted_name": convertedPlaylistNameForWeaviate,
                "playlist_Url": f'https://www.youtube.com/playlist?list={playlistId}'
                })
            
            newData.append({
                "playlist_name": orignalPlaylistName, 
                "converted_name": convertedPlaylistNameForWeaviate,
                "playlist_Url": f'https://www.youtube.com/playlist?list={playlistId}'
                })
            
            newDataAddedToJsonFile = True  # Set the flag to True

    # Save the updated playlist data back to the JSON file only if new data is added
    if newDataAddedToJsonFile:
        savePlaylistDataInJsonFile(playlistData, jsonFilePath)
        print(f"\nPlaylist data saved to {jsonFilePath}")
        return newData
    else:
        print("\nNo new data added. Playlist data not saved.")
        return False
    

# Example usage:
# playlistIds = [
#     "PLNxd9fYeqXeapl8xZGkdF2aBq_jp67Wya",
#     "PLNxd9fYeqXebPQ7ZHJWYYrxCVjvPoOuJV",
#     "PLNxd9fYeqXeYEKumYSWXIGMfTX1qeyxDK",
#     "PLNxd9fYeqXeYvBUgN7PyVae0R665TJ9eB"
# ]

# json_file_path_example = "outputJSON/WeaviateClassName.json"

# data = checkPlaylistData(playlistIds, json_file_path_example)
# print(data)
