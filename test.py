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
    


video_url = "https://dw3htsev2ue75.cloudfront.net/file_library/videos/vod_non_drm_ios/3877970/1701868520_9313420424950984/1701868505553_509274441213191230_video_VOD.m3u8"
start_time_seconds = 220.139

# Append the start time parameter to the video URL
modified_video_url = f"{video_url}#t={start_time_seconds}"

# Now you can use the modified_video_url in your Streamlit UI
print(modified_video_url)


