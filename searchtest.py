import os
import weaviate
from dotenv import load_dotenv
from src.textToVectors import convertTextToVectors
import pprint

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
# WEAVIATE_CLASS_NAME = os.getenv("WEAVIATE_CLASS_NAME")
# weaviateClassName = os.getenv("WEAVIATE_CLASS_NAME")


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

# max_distance = 0.16

# def searchData(question,number,weaviateClassName):
#     vectors = convertTextToVectors(question)
#     response = (
#         client.query
#         .get(f"{weaviateClassName}", ["text","videoUrl","start","duration"])
#         .with_near_vector({
#             "vector": vectors[0],
#             # "distance": max_distance
#             })
#         # .with_limit(5)
#         .with_limit(number)
#         # .with_offset(1)
#         .with_additional(["distance"])
#         # .with_additional("vector")

#         .do()
#         )
#     return(response)


def searchData(question,number,weaviateClassName):
    vectors = convertTextToVectors(question)
    response = (
        client.query
        .get(f"{weaviateClassName}", ["text","videoUrl","start","duration"])
        .with_near_vector({
            "vector": vectors[0],
            # "distance": max_distance
            })
        # .with_limit(5)
        .with_limit(number)
        # .with_offset(1)
        # .with_additional(["distance"])
        .with_additional('rerank(property: "text" query: newtons third law) { score }')

        .do()
        )
    return(response)


# def searchData(question,number,weaviateClassName):
#     vectors = convertTextToVectors(question)
#     response = (
#         client.query
#         .get(f"{weaviateClassName}", ["text","videoUrl","start","duration"])
#         .with_hybrid(
#         query=question,
#         vector=vectors[0]
#     )
#         # .with_limit(5)
#         .with_limit(number)
#         # .with_offset(1)
#         .with_additional(["distance"])

#         .do()
#         )
#     return(response)


weaviateClassName = "PhysicsLaw"

question = "newtons third law"
res = searchData(question,5,weaviateClassName)
print("\n------------------search start------------------------\n")
# pprint.pprint(res)
print(res)
print("\n------------------search end------------------------\n")