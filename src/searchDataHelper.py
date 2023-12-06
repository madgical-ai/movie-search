import os
import weaviate
from dotenv import load_dotenv
from .textToVectors import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
weaviateClassName = os.getenv("WEAVIATE_CLASS_NAME")


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
def searchData(question,number,weaviateClassName):
    vectors = convertTextToVectors(question)
    response = (
        client.query
        .get(f"{weaviateClassName}", ["text","videoUrl","start","duration"])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
        .do()
        )
    return(response)
