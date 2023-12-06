import weaviate
import json

client = weaviate.Client(url="http://13.127.55.84:2400")
print("\nbefore delete -------")
schema = client.schema.get()
for i in schema["classes"]:
    print(i["class"])

all_objects = client.data_object.get(class_name="PhysicsLaw")
with open(f'outputJSON/PhysicsLaw.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
    

