import weaviate
import os
from dotenv import load_dotenv
import pprint
from src.youtubePlaylistDataManager import loadPlaylistDataFromJsonFile
import json

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
client = weaviate.Client(WEAVIATE_CLUSTER_URL)
schema = client.schema.get()
jsonFilePath = "outputJSON/WeaviateClassName.json"

def deleteUnmatchData(jsonFilePath,schema):

    playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)

    # print("\n playlistData  ------------------------------------  ")
    # pprint.pprint(playlistData)

    # Get all Weaviate class names
    weaviate_classes = [class_entry["class"] for class_entry in schema["classes"]]

    # Iterate through JSON data and check for matches
    unmatched_entries = []
    for playlistEntry in playlistData:
        if playlistEntry["converted_name"] not in weaviate_classes:
            unmatched_entries.append({
                "playlist_name": playlistEntry["playlist_name"],
                "converted_name": playlistEntry["converted_name"],
                "playlist_Url": playlistEntry["playlist_Url"]
            })

    # Delete unmatched entries from JSON file
    if unmatched_entries:
        # print("\nUnmatched Entries:  ------------------------------------------")
        # pprint.pprint(unmatched_entries)

        # Remove unmatched entries from the JSON file
        updated_data = [entry for entry in playlistData if entry["converted_name"] not in [unmatched["converted_name"] for unmatched in unmatched_entries]]
        with open(jsonFilePath, "w") as json_file:
            json.dump(updated_data, json_file, indent=4)

        print("\nDeleted unmatched entries from the JSON file.")

    else:
        print("\nNo unmatched entries found.")

    # playlistData = loadPlaylistDataFromJsonFile(jsonFilePath)

    # print("\n playlistData after deleating un matched  ------------------------------------  ")
    # pprint.pprint(playlistData)