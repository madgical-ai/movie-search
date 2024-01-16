import os
import weaviate
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")

text_model = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)


def textToVectorSentenceTransformer(text):
    texts = [text]
    text_embeddings = text_model.encode(texts)
    return text_embeddings


def searchImages(question, number):
    # vectors = convertTextToVectors(question)
    vectors = textToVectorSentenceTransformer(question)
    response = (
        client.query.get(
            f"{IMAGE_WEAVIATE_CLASS_NAME}",
            # ["Name", "imagePath", "time", "video_url", "video_url_with_time"],
            ["imagePath", "time", "video_url", "video_url_with_time"],
        )
        .with_near_vector({"vector": vectors[0], "certainty": 0.62})
        .with_limit(1000)
        # .with_limit(number)
        .with_additional(["certainty"])
        .do()
    )
    return response
