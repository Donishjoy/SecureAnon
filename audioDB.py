import os
from moviepy.editor import *
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")  
db = client["face"]
frames_collection = db["Anonymize"]
video_info_collection = db["video_info"]

def extract_audio(video_path,video_id):
        output_audio_file=os.path.join("uploads",f"{video_id}.mp3")
        video_clip=VideoFileClip(video_path)
        audio_clip=video_clip.audio
        audio_clip.write_audiofile(output_audio_file)
        video_info_data = {
            "video_id": video_id,
            "audio_path": output_audio_file,
            "output_path":"" 
        }

        # Insert video info data into "video_info" collection
        video_info_collection.insert_one(video_info_data)

def combine_audio(video_id):
    data = video_info_collection.find_one({'video_id': video_id})
    print("data", data)
    audio_path = data['audio_path']
    video_path = data['output_path']
    print(audio_path)
    print(video_path)
    clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    videoclip = clip.set_audio(audio_clip)
    new_filename = os.path.splitext(video_path)[0] + "_with_audio.mp4"
    videoclip.write_videofile(new_filename, codec="libx264", audio_codec="aac")
    
    return new_filename
