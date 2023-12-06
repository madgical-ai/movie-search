import streamlit as st
import os
import weaviate
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer, util
from PIL import Image


load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
IMAGE_WEAVIATE_CLASS_NAME = os.getenv("IMAGE_WEAVIATE_CLASS_NAME")


text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')


# Website Fonts and Title
# st.set_page_config(page_title="Video Search", page_icon="🐍", layout="wide")
st.set_page_config(page_title="Image Search", page_icon="🐍")
# st.title("Video Search Tool")
st.markdown("<h1 style='text-align: center;'>Image Search</h1>", unsafe_allow_html=True)
# Add space below the title
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)


def textToVectorSentenceTransformer(text):
    texts = [text]
    text_embeddings = text_model.encode(texts)
    return text_embeddings

# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

def searchImages(question,number):
    # vectors = convertTextToVectors(question)
    vectors = textToVectorSentenceTransformer(question)
    response = (
        client.query
        .get(f"{IMAGE_WEAVIATE_CLASS_NAME}", ["imagePath"])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
        .do()
        )
    return(response)

container0 = st.container()
container1 = st.container()

# Initialize an empty DataFrame
imageResponse = None  # Move the declaration outside the button block

# Initialize an empty DataFrame
with container0:

        # Input box for the question and number with default number value
        question = st.text_input("Enter your Image Search Query")
        number = st.number_input("Number of Search Results", value=5)

        #  For button
        if st.button("Search Image"):
            # print("------------------------------------------------------")
            # print(question)
            # print("--------------------------------")
            with st.spinner("Searching...."):
                try:
                    imageResponse = searchImages(question,number)
                    # st.write(response)
                except Exception as e:
                     st.warning(f"An error occurred: {e}")

with container1:
        st.subheader('Search Results', divider='rainbow')
        # Check if response is not None before accessing it
        if imageResponse is not None:
            image_data = imageResponse["data"]["Get"][IMAGE_WEAVIATE_CLASS_NAME]
            image_paths = [entry['imagePath'] for entry in image_data]

            for path in image_paths:
                st.image(path)