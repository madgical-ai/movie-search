import weaviate
import os
from dotenv import load_dotenv
import pprint
import weaviate.exceptions


load_dotenv()

WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")

client = weaviate.Client(WEAVIATE_CLUSTER_URL)
# client.schema.delete_all()

print("\nbefore delete -------")
schema = client.schema.get()
for i in schema["classes"]:
    print(i["class"])

# client.schema.delete_class("VideoCriptImageData")
# client.schema.delete_class("VideoCriptTextData2")
# client.schema.delete_class("ArcticVets_NatGeoWILD")
# client.schema.delete_class("ImagesData")
# client.schema.delete_class("PhysicsLaw")
# client.schema.delete_class("TopWILDSharkMoments_NatGeoWILD")
# client.schema.delete_class("TheHatcherFamilyDairy_NatGeoWILD")
# client.schema.delete_class("WizardofPaws_NatGeoWILD")

print("\nafter delete -------")
schema = client.schema.get()
for i in schema["classes"]:
    print(i["class"])
