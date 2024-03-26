import cv2
import os
import pymongo
import easyocr
import face_recognition

# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Anonymize"]  # Replace with your collection name

output_folder = os.path.join("frames")
video_id = "01"  # Set the video ID here

# Function to extract frames, detect text, save frames, and add details to MongoDB
def save_frames_to_db(video_path, video_id, reference_image_path):

    # Initialize easyOCR reader with GPU
    reader = easyocr.Reader(['en'], gpu=True)
    print("CompareDB")
    print("videoid",video_id," video_path",video_path)
    # Load the reference image for face recognition
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

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

        # Read text from the frame
        result = reader.readtext(frame)

        # Find face locations in the current frame
        face_locations = face_recognition.face_locations(frame)

        # Process each detected text and face in the frame
        text_objects = []
        blur_objects = []

        for detection in result:
            top_left = tuple([int(val) for val in detection[0][0]])
            bottom_right = tuple([int(val) for val in detection[0][2]])
            text = detection[1]

            # Add text location to the list
            text_objects.append({"top": top_left[1], "right": bottom_right[0], "bottom": bottom_right[1], "left": top_left[0], "text": text})

        # Check for matches with the reference face
        for loc in face_locations:
            current_encoding = face_recognition.face_encodings(frame, [loc])[0]
            match = face_recognition.compare_faces([reference_encoding], current_encoding)

            if match[0]:
                # Add face location to the list for blur
                blur_objects.append({"top": loc[0], "right": loc[1], "bottom": loc[2], "left": loc[3], "is_reference_face": True})
            else:
                continue  # Skip non-matching faces

        # Merge text and matching face locations for blur
        blur_objects.extend(text_objects)

        # Prepare update query for MongoDB to update the "blur" field
        update_query = {"frame_number": count, "video_id": video_id}
        new_values = {"$set": {"blur": blur_objects}}

        # Update the "blur" field in MongoDB for the current frame
        frames_collection.update_one(update_query, new_values)
        print(count)
        count += 1

# Driver code
if __name__ == "__main__":

    video_path = input("Enter the path to the video file: ")
    reference_image_path = input("Enter the path to the reference image: ")

    save_frames_to_db(video_path,  video_id, reference_image_path)

    print(f"Blur details updated in MongoDB collection '{frames_collection.name}' for video ID '{video_id}'.")
