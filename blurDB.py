import cv2
import os
import face_recognition
import numpy as np
import pymongo

# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Anonymize"]  # Replace with your collection name

output_folder = os.path.join("comparison")
video_id = "03"  # Set the video ID here

# Function to blur faces based on face locations and save frames to a folder
def blur_and_save_frames(video_path):

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

        # Retrieve frame data from MongoDB based on frame number and video ID
        frame_data = frames_collection.find_one({"frame_number": count, "video_id": video_id})

        if frame_data:
            face_locations = frame_data.get("blur", [])  # Get face locations

            for loc in face_locations:
                top, right, bottom, left = loc["top"], loc["right"], loc["bottom"], loc["left"]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Draw rectangle around face
                
                # Blur the face location
                face = frame[top:bottom, left:right]  # Crop the face
                face = cv2.GaussianBlur(face, (99, 99), 60)  # Adjust the kernel size and sigma as needed
                frame[top:bottom, left:right] = face  # Replace the face with the blurred face

            comparison_frame_path = os.path.join(output_folder, f"frame_{count}_blurred.jpg")
            cv2.imwrite(comparison_frame_path, frame)

        count += 1

# Driver code
if __name__ == "__main__":

    video_path = input("Enter the path to the video file: ")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    blur_and_save_frames(video_path)

    print(f"All frames saved in '{output_folder}' folder.")
