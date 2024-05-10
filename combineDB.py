import cv2
import os
import pymongo
import datetime
# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Anonymize"]  # Replace with your collection name
video_info_collection = db["video_info"]
output_folder = "comparison"
video_id = "03"  # Set the video ID here
destination="output"
# Function to combine frames based on start time and end time from MongoDB
def combine_frames_from_db(currentuser,video_id):
    frames = []
    start_times = []
    end_times = []
    print("combineDB")
    # Retrieve frame data from MongoDB and store frames, start times, and end times
    for frame_data in frames_collection.find({"video_id": video_id}).sort("frame_number"):
        frame_path = os.path.join(output_folder, f"frame_{frame_data['frame_number']}_blurred.jpg")
        if os.path.exists(frame_path):
            frame = cv2.imread(frame_path)
            frames.append(frame)
            start_times.append(frame_data['start_time'])  # Assuming 'start_time' field in MongoDB represents frame start time
            end_times.append(frame_data['end_time'])  # Assuming 'end_time' field in MongoDB represents frame end time

    # Combine frames based on start time and end time
    if frames:
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        video_filename = os.path.join(destination, f"video_{currentuser+timestamp}.mp4")  # Construct video filename
        video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (width, height))

        for frame, start_time, end_time in zip(frames, start_times, end_times):
            # Perform operations based on start and end times if needed
            video_writer.write(frame)

        video_writer.release()
        print("Frames combined into 'combined_video.mp4'.")
        update_query={"video_id":video_id}
        new_values = {"$set": {"output_path": video_filename}}
        video_info_collection.update_one(update_query,new_values)
        return video_filename
# Driver code
if __name__ == "__main__":
    combine_frames_from_db()