import weaviate
import os
import json
from dotenv import load_dotenv
from src.imageToVector import convertImageToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")
# WEAVIATE_CLASS_NAME = "imageDatabase"


def pushImageDataToWeaviate(data):
    # Your JSON data with a larger number of items
    print("\nImage Data Lenth (array of dictonary -  )", len(data))

    # Initialize Weaviate client
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

    # Get the current schema
    schema = client.schema.get()
    print("\n---------------------weaviate schema--------------------")
    # print(schema)
    for i in schema["classes"]:
        print(i["class"])

    print("---------------------weaviate schema--------------------\n")
    client.schema.delete_class(IMAGE_WEAVIATE_CLASS_NAME)
    schema = client.schema.get()

    for i in schema["classes"]:
        print(i["class"])
    print("---------------------weaviate schema--------------------\n")

    # Check if the class already exists
    class_exists = any(
        cls["class"] == IMAGE_WEAVIATE_CLASS_NAME for cls in schema["classes"]
    )

    # Define the class name and schema
    # client.schema.delete_all()
    # client.schema.delete_class(IMAGE_WEAVIATE_CLASS_NAME)
    class_obj = {
        "class": IMAGE_WEAVIATE_CLASS_NAME,
        "vectorizer": "none",
        "moduleConfig": {},
    }

    # Create the class in Weaviate or check if it exixt or not
    try:
        if not class_exists:
            client.schema.create_class(class_obj)
            print(f"Class '{IMAGE_WEAVIATE_CLASS_NAME}' created successfully.")
    except weaviate.RequestError as e:
        if e.status_code == 409:
            print(f"Class '{IMAGE_WEAVIATE_CLASS_NAME}' already exists.")
        else:
            print(f"Error creating class: {e}")

    # Split your data into batches
    batch_size = 30
    data_batches = [data[i : i + batch_size] for i in range(0, len(data), batch_size)]
    print("\n Batch Data lenth -  ", len(data_batches))

    # Initialize a counter for imported data
    imported_count = 0

    for batch_index, batch_data in enumerate(data_batches):
        # print("image paths  -  ",batch_data)
        print(f"\nImporting segment: Batch {batch_index + 1}")
        with client.batch as batch:
            for i, d in enumerate(batch_data):
                try:
                    # print(f"Importing segment: {i + 1} in batch {batch_index + 1}")
                    properties = {
                        "imagePath": d["image_path"],
                        "time": d["time"],
                        "video_url": d["video_url"],
                        "video_url_with_time": d["video_url_time"],
                    }
                    # Tokenize the image for vector search
                    vec = convertImageToVectors(d["image_path"])

                    batch.add_data_object(
                        data_object=properties,
                        class_name=IMAGE_WEAVIATE_CLASS_NAME,
                        vector=vec,
                    )
                    imported_count += 1
                except Exception as e:
                    print(
                        f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}"
                    )

    print("Image Data import completed.")

    all_objects = client.data_object.get(class_name=IMAGE_WEAVIATE_CLASS_NAME)
    with open(
        f"output/{IMAGE_WEAVIATE_CLASS_NAME}-From-Weaviate.json", "w", encoding="utf-8"
    ) as json_file:
        json.dump(all_objects, json_file, ensure_ascii=False, indent=4)

    return "done"
