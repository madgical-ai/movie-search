import os
import weaviate
from dotenv import load_dotenv
from .textToVectors import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")
max_distance = 0.11
min_certainty = 0.85

# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
max_distance = 0.11
def searchData(question,number):
    vectors = convertTextToVectors(question)
    response = (
        client.query
        .get(f"{VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME}", ["text","title","start_time_in_seconds","video_download_url","video_file_url_hls"])
        .with_near_vector({
            "vector": vectors[0],
            # "certainty": 0.9  # Adjust certainty based on your requirements
            "certainty": 0.85  # Adjust certainty based on your requirements
            # "distance": max_distance
            
            })
        # .with_limit(5)
        .with_limit(number)
        # .with_additional(["distance"])
        .with_additional(["certainty"])
        .do()
        )
    print(response)
    return(response)


# def searchData(question, number):
#     vectors = convertTextToVectors(question)
#     response = (
#         client.query
#         .get(f"{VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME}", ["text", "title", "start_time_in_seconds", "video_download_url", "video_file_url_hls"])
#         .with_near_vector({
#             "vector": vectors[0],
#             "distance": max_distance,
#             "certainty": min_certainty
#         })
#         .with_limit(number)
#         .with_additional(["distance", "certainty"])
#         .do()
#     )
#     print(response)
#     return response