import cv2
import numpy as np
import os

class ModelParams():
    mean = [104, 117, 123]
    scale = 1.0
    in_width = 300
    in_height = 300
    

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
