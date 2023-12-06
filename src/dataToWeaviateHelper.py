import weaviate
import os
import json
from dotenv import load_dotenv
from .textToVectors import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")

def pushDataToWeaviate(data,weaviateClassName):
    
    # Your JSON data with a larger number of items
    print(len(data))

    # Initialize Weaviate client
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

    # client.schema.delete_all()

    # Define the class name and schema
    client.schema.delete_class(weaviateClassName)

    class_obj = {
        "class": weaviateClassName,
        "vectorizer": "none",
        "moduleConfig": {}
    }

    # Create the class in Weaviate
    try:
        client.schema.create_class(class_obj)
        print(f"Class '{weaviateClassName}' created successfully.")
    except weaviate.RequestError as e:
        if e.status_code == 409:
            print(f"Class '{weaviateClassName}' already exists.")
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
                        "videoUrl": d["video_url"],
                        "title": d["title"],
                        "author": [d["author"]],  # Fix author field
                        "text": d["text"],
                        "start": d["start"],
                        "duration": d["duration"],
                    }
                    vec = convertTextToVectors(d["text"])
                    batch.add_data_object(
                        data_object=properties,
                        class_name=weaviateClassName,
                        # vector=embeddings[i].tolist()
                        vector=vec[0]
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}")

    print("Data import completed.")

    all_objects = client.data_object.get(class_name=weaviateClassName)
    with open(f'outputJSON/{weaviateClassName}.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
    
    return "done"    