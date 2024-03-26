import cv2
import os
import dlib
import pymongo
import datetime
# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Anonymize"]  # Replace with your collection name

output_folder = os.path.join("frames")
  # Set the video ID here
video_id='1'
# Initialize dlib's GPU face detector (if available)
dlib.DLIB_USE_CUDA = True

# Function to extract frames, detect faces, save frames, and add details to MongoDB
def save_frames_to_db(video_path, output_folder, video_id,currentuser):

    # Path to video file
    vid_obj = cv2.VideoCapture(video_path)

    # Counter variable
    count = 0

    # Create a face detector
    face_detector = dlib.get_frontal_face_detector()

    # Check for successful frame extraction
    success = True

    while success:

        # Extract a frame from the video
        success, frame = vid_obj.read()

        # Break the loop if no frames are extracted
        if not success:
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the current frame using dlib's GPU-accelerated face detector
        face_rects = face_detector(gray_frame, 0)

        # Convert dlib rectangles to face location tuples
        face_locations = [(rect.top(), rect.right(), rect.bottom(), rect.left()) for rect in face_rects]

        # Skip frames without faces
        if not face_locations:
            continue

        # Encode faces in the current frame and calculate frame duration (assuming constant FPS)
        frame_duration = 1 / vid_obj.get(cv2.CAP_PROP_FPS)  # Assuming constant FPS
        # Save the frame in the "frames" folder
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        frame_path = os.path.join(output_folder, f"frame_{currentuser+timestamp}_{count}.jpg")
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
