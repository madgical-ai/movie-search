import weaviate
import os
import json
from dotenv import load_dotenv
from .textToVectors import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME = os.getenv("VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME")


jsonFolder = "output"
os.makedirs(jsonFolder, exist_ok=True)
def pushDataToWeaviate(data):
    
    # Your JSON data with a larger number of items
    print(len(data))

    # Initialize Weaviate client
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

    # client.schema.delete_all()

    # Define the class name and schema
    client.schema.delete_class(VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME)

    class_obj = {
        "class": VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME,
        "vectorizer": "none",
        "moduleConfig": {}
    }


    # class_obj = {
    #     "class": VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME,
    #     "vectorizer": "none",
    #     "vectorIndexConfig": {
    #     "distance": "dot",
    # },
    #     "moduleConfig": {}
    # }

    # Create the class in Weaviate
    try:
        client.schema.create_class(class_obj)
        print(f"Class '{VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME}' created successfully.")
    except weaviate.RequestError as e:
        if e.status_code == 409:
            print(f"Class '{VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME}' already exists.")
        else:
            print(f"Error creating class: {e}")


    # Tokenize the input texts
    # embeddings, data_batches = convertTextToVectors(data)

    # Split your data into batches
    batch_size = 10
    data_batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
    print("\n Batch Data lenth -  ",len(data_batches))

    # Initialize a counter for imported data
    imported_count = 0

    for batch_index, batch_data in enumerate(data_batches):
        print(f"\nImporting segment: Batch {batch_index + 1}")
        with client.batch as batch:
            for i, d in enumerate(batch_data):
                try:
                    # print(f"Importing segment: {i + 1} in batch {batch_index + 1}")
                    properties = {
                        "title": d["title"],
                        "video_id": d["video_id"],
                        "start_time": d["start_time"],
                        "end_time": d["end_time"],
                        "text": d["text"],
                        "start_time_in_seconds": d["start_time_in_seconds"],
                        "total_video_Duration": d["total_video_Duration"],
                        "video_file_url_hls": d["video_file_url_hls"],
                        "video_download_url": d["video_download_url"],
                        "original_url": d["original_url"],
                    }
                    vec = convertTextToVectors(d["text"])
                    batch.add_data_object(
                        data_object=properties,
                        class_name=VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME,
                        # vector=embeddings[i].tolist()
                        vector=vec[0]
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}")

    print("Data import completed.")

    all_objects = client.data_object.get(class_name=VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME)
    with open(f'{jsonFolder}/{VIDEO_CRIPT_TEXT_WEAVIATE_CLASS_NAME}-From-Weaviate.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
    
    return "done"    