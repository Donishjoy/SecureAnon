import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory,json
from flask_cors import CORS
import os
from pymongo import MongoClient
import pymongo 
import shutil
import math
import framesDB
import compareDB
import blurDB
import combineDB
# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Image"]  # Replace with your collection name
selective_collection=db["Selective"]

class ModelParams():
    mean = [104, 117, 123]
    scale = 1.0
    in_width = 300
    in_height = 300

class FaceBlurApp:
    __face_detector = None
    __model_params = None
    __max_blur_factor = 5
    __min_blur_factor = 1

    def __init__(self):
        self.__loadModel()

    def run(self, image_path, output_path, blur_factor):
        image = cv2.imread(image_path)
        faces = self.__detectFaces(image)
        output_image = self.__blurFaces(image, faces, blur_factor)

        cv2.imwrite(output_path, output_image)
        return(faces)
        
        

    def __detectFaces(self, image):
        blob = cv2.dnn.blobFromImage(image, scalefactor=self.__model_params.scale, size=(self.__model_params.in_width, self.__model_params.in_height),
                                      mean=self.__model_params.mean, swapRB=False, crop=False)
        self.__face_detector.setInput(blob)
        detections = self.__face_detector.forward()

        height, width = image.shape[:2]
        detected_faces = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence >= 0.5:  # Adjust the confidence threshold as needed
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")
                detected_faces.append({'index':i, 'coordinates': [x1, y1, x2, y2]}) 

        return detected_faces
    def __blurFaces(self, image, faces, blur_factor):
        blurred_image = image.copy()
        for face in faces:  # Iterate directly over the faces list
            (x1, y1, x2, y2) = face['coordinates']  # Access coordinates using correct key
            face_roi = image[y1:y2, x1:x2]
            blurred_face = self.__blurFace(face_roi, blur_factor)
            blurred_image[y1:y2, x1:x2, :] = blurred_face
        return blurred_image

    def __blurSelectedFaces(self, image, faces, blur_factor, selected_faces):
        blurred_image = image.copy()
        for i, (x1, y1, x2, y2) in enumerate(faces):
            if i in selected_faces:
                face = image[y1:y2, x1:x2]
                face = self.__blurFace(face, blur_factor)
                blurred_image[y1:y2, x1:x2, :] = face
        return blurred_image


    def __blurFace(self, face, blur_factor):
        height, width = face.shape[:2]
        w_k = int(width / ((self.__max_blur_factor + 1) - blur_factor))
        h_k = int(height / ((self.__max_blur_factor + 1) - blur_factor))
        if w_k % 2 == 0:
            w_k += 1
        if h_k % 2 == 0:
            h_k += 1

        if face.shape[0] != 0 and face.shape[1] != 0:
            blurred = cv2.GaussianBlur(face, (w_k, h_k), 0)
        else:
            blurred = face

        return blurred

    def __loadModel(self):
        self.__face_detector = cv2.dnn.readNetFromCaffe('model/deploy.prototxt', 'model/res10_300x300_ssd_iter_140000.caffemodel')
        self.__model_params = ModelParams()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
STATIC_FOLDER='static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
@app.route('/api/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    blur_factor = int(request.form.get('blur_factor', 3))  # Default blur factor is 3
    blur_all_faces = request.form.get('blur_all_faces', 'true').lower() == 'true'

    face_blurrer = FaceBlurApp()
    output_filename = 'blurred_' + file.filename
    print(output_filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    faces=face_blurrer.run(file_path, output_path, blur_factor)
    print(faces)
    image_data={
    'userId': 1,
    'image_path': file_path,
    'output_path': output_path,
    'blur_factor': blur_factor,
    'faces': [{'coordinates': [int(x) for x in face['coordinates']]} for face in faces]  # Convert coordinates to integers
    }
    frames_collection.insert_one(image_data)
    return jsonify({'message': 'File processed successfully', 'output_path': output_path}), 200

# Serve the processed files
class FaceDetector:
    def __init__(self):
        self.__loadModel()

    def __loadModel(self):
        self.__face_detector = cv2.dnn.readNetFromCaffe('model/deploy.prototxt', 'model/res10_300x300_ssd_iter_140000.caffemodel')
        self.__model_params = ModelParams()

    def detect_faces(self, image_path):
        image = cv2.imread(image_path)
        blob = cv2.dnn.blobFromImage(image, scalefactor=self.__model_params.scale, size=(self.__model_params.in_width, self.__model_params.in_height),
                                      mean=self.__model_params.mean, swapRB=False, crop=False)
        self.__face_detector.setInput(blob)
        detections = self.__face_detector.forward()

        height, width = image.shape[:2]
        detected_faces = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence >= 0.5:  # Adjust the confidence threshold as needed
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")
                detected_faces.append({'coordinates': [x1, y1, x2, y2]})  # Convert tuple to list
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle
                cv2.putText(image, str(i), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)  # Put index number
                
        file_name = os.path.basename(image_path)
        save_path = os.path.join(os.path.dirname(image_path), file_name)
        cv2.imwrite(save_path, image)
        print(detected_faces)
        return detected_faces

    def blurFaces(self, image, faces, blur_factor):
        blurred_image = image.copy()
        for (x1, y1, x2, y2) in faces:
            face = image[y1:y2, x1:x2]
            face = self.__blurFace(face, blur_factor)
            blurred_image[y1:y2, x1:x2, :] = face
        return blurred_image

    def blurSelectedFaces(self, image, faces, blur_factor, selected_faces):
        blurred_image = image.copy()
        for i, (x1, y1, x2, y2) in enumerate(faces):
            if i in selected_faces:
                face = image[y1:y2, x1:x2]
                face = self.blurFaces(face, blur_factor)
                blurred_image[y1:y2, x1:x2, :] = face
        return blurred_image

@app.route('/api/face', methods=['POST'])
def uploads_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    f1=request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
    file.save(file_path)
    print("f1",f1.filename)
    static_path=os.path.join(app.config['STATIC_FOLDER'],f1.filename)
    shutil.copy(file_path,static_path)
    face_detector = FaceDetector()
    detected_faces = face_detector.detect_faces(file_path)
    print('face_detector detected',detected_faces)
    # Convert int32 values to Python integers for JSON serialization
    for face_list in detected_faces:
            face_list['coordinates'] = [int(coord) for coord in face_list['coordinates']]

    # Extract only the indices from the detected_faces list
    

    # Prepare a response JSON object including detected faces data
    response_data = {
        
        'detected_faces': detected_faces,
        'image_path': file_path
    }   
    selective_image={
        'userId':1,
        'image_path':file_path,
        'faces':detected_faces,
        'static_path':static_path}
    
    selective_collection.insert_one(selective_image)
    return jsonify(response_data), 200

@app.route('/api/selected-faces', methods=['POST'])
def select():
    selected_data = request.json
    print(selected_data)

    selected_faces = selected_data['selectedFaces']  # List of selected face indices
    file_path = selected_data['selectedFile']  # Optional: original file path (if needed)
    image_path = selected_data['imagePath']  # Path to the image to be blurred
    blur_factor = int(selected_data.get('blurFactor', 3))  # Default blur factor is 3

    # Retrieve detected faces from the database
    detected_faces = selective_collection.find_one({"image_path": image_path})
    if detected_faces is None:
        return jsonify({'error': 'No face data found for the image'}), 400

    faces = detected_faces['faces']
    static_path=detected_faces['static_path']# List of face data (including index and coordinates)
    # Blur selected faces
    output_image = cv2.imread(static_path)  # Read the image
    blurred_image = output_image.copy()
    for index, face in enumerate(faces):
        if index in selected_faces:  # Check if face index is in selected list
            face_roi = output_image[face['coordinates'][1]:face['coordinates'][3],
                                    face['coordinates'][0]:face['coordinates'][2]]

            # Adjust sigma based on blur factor (modify as needed)
            kernel_size = 5  # Adjust kernel size as needed (should be odd)
            sigma = blur_factor * math.log(blur_factor + 1, 2)  # Scale blur factor (adjust multiplier if needed)
            blurred_face = cv2.GaussianBlur(face_roi, (kernel_size, kernel_size), sigma, sigma)

            blurred_image[face['coordinates'][1]:face['coordinates'][3],
                           face['coordinates'][0]:face['coordinates'][2], :] = blurred_face

    # Save and return the result (modify as needed)
    output_filename = 'blurred_' + os.path.basename(image_path)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    cv2.imwrite(output_path, blurred_image)

    return jsonify({'message': 'Faces blurred successfully', 'output_path': output_path}), 200




@app.route('/output/<path:filename>')
def get_processed_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/uploads/<path:filename>')
def get_face_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/videoupload',methods=['POST'])
def video_upload():
        if 'file' not in request.files:
            return jsonify({'error':'No file part'}), 400
        file=request.files['file']
        if file.filename=='':
            return jsonify({'error':'No file is selected'}), 400
        file_path=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(file_path)
        output_folder = os.path.join("frames")
        video_id = "03"  # Set the video ID here
        framesDB.save_frames_to_db(file_path,output_folder,video_id)
        return jsonify({'file_path':file_path,'video_id':video_id})
    
@app.route('/api/reference', methods=['POST'])
def reference():
    # Check if 'file' exists in request.files
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    # Get the file from the request
    file = request.files['file']
    
    # Check if a file was provided
    if file.filename == '':
        return jsonify({'error': 'No file is selected'}), 400
    
    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Get other data from the request body
    video_path = request.form['video_path']
    video_id = request.form['video_id']
    
    # Perform further processing (assuming compareDB is defined somewhere)
    
    blurDB.blur_and_save_frames(video_path)
    output_file=combineDB.combine_frames_from_db()
    print("file",output_file)
    return jsonify({'success': 'Video has been compared.','output': output_file})
    
    
if __name__ == '__main__':
    app.run(debug=True)
