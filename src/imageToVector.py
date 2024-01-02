from sentence_transformers import SentenceTransformer, util
from PIL import Image, ImageFile
import os
import torch
import torch.nn.functional as F
from torch import Tensor
# from src.textToVectors import convertTextToVectors

# We use the original clip-ViT-B-32 for encoding images
img_model = SentenceTransformer('clip-ViT-B-32')

# Now we load and encode the images
def load_image(path):
    return Image.open(path)


def convertImageToVectors(imgPath):
    
    image = load_image(imgPath)
    # print(imgPath)

    # Map images to the vector space all at once
    # img_embeddings = img_model.encode(images)
    # print("Image embed")

    # Map images to the vector space one by one 
    img_embeddings = img_model.encode(image)


    return img_embeddings
    

