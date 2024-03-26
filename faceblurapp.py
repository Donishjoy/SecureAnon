import cv2
import numpy as np
import os
import easyocr
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
        reader = easyocr.Reader(['en'], gpu=True)
        result=reader.readtext(blurred_image)
        text_objects = []
        for detection in result:
            top_left = tuple([int(val) for val in detection[0][0]])
            bottom_right = tuple([int(val) for val in detection[0][2]])
            text = detection[1]
            # Add text location to the list
            text_objects.append({"top": top_left[1], "right": bottom_right[0], "bottom": bottom_right[1], "left": top_left[0], "text": text})
        for face in faces:  # Iterate directly over the faces list
            (x1, y1, x2, y2) = face['coordinates']  # Access coordinates using correct key
            face_roi = image[y1:y2, x1:x2]
            blurred_face = self.__blurFace(face_roi, blur_factor)
            blurred_image[y1:y2, x1:x2, :] = blurred_face
            
            # Text location blurring
        for text_obj in text_objects:
            mask = np.zeros(blurred_image.shape[:2], np.uint8)
            # Create mask based on text_obj coordinates (e.g., cv2.rectangle)
            x1,y1,x2,y2=text_obj['left'], text_obj['top'],text_obj['right'], text_obj['bottom']
            text_region=image[y1:y2,x1:x2]
            blurred_img=self.__blurFace(text_region,blur_factor)
            blurred_image[y1:y2, x1:x2, :] = blurred_img
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