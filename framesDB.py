import cv2
import os
import face_recognition
import pymongo

# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Anonymize"]  # Replace with your collection name

output_folder = os.path.join("frames")
video_id = "01"  # Set the video ID here

# Function to extract frames, detect faces, save frames, and add details to MongoDB
def save_frames_to_db(video_path, output_folder, video_id):

    # Path to video file
    vid_obj = cv2.VideoCapture(video_path)


    # Counter variable
    count = 0

    # Check for successful frame extraction
    success = True

    while success:

        # Extract a frame from the video
        success, frame = vid_obj.read()

        # Break the loop if no frames are extracted
        if not success:
            break

        # Find face locations in the current frame
        face_locations = face_recognition.face_locations(frame)

        # Skip frames without faces
        if not face_locations:
            continue

        # Encode faces in the current frame and calculate frame duration (assuming constant FPS)
        frame_encodings = face_recognition.face_encodings(frame, face_locations)
        frame_duration = 1 / vid_obj.get(cv2.CAP_PROP_FPS)  # Assuming constant FPS
        # Save the frame in the "frames" folder
        frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, frame)

        # Prepare frame data for MongoDB
        frame_data = {
            "frame_number": count,
            "video_id": video_id,
            "start_time": (count * frame_duration) - frame_duration,  # Account for previous frame duration
            "end_time": count * frame_duration,
            "resolution": (vid_obj.get(cv2.CAP_PROP_FRAME_WIDTH), vid_obj.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "blur": [],  # Placeholder for blur detection (implementation not provided)
            "faces": face_locations,
        }

        # Insert frame data into MongoDB
        frames_collection.insert_one(frame_data)

        count += 1

# Driver code
if __name__ == "__main__":

    video_path = input("Enter the path to the video file: ")

    save_frames_to_db(video_path, output_folder, video_id)

    print(f"All frames saved in '{output_folder}' folder.")
    print(f"Frame details with video ID '{video_id}' added to MongoDB collection '{frames_collection.name}' in database '{db.name}'.")