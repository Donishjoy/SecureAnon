
SecureAnon is a pioneering initiative aimed at tackling the escalating concerns surrounding personal privacy in today's digital era. Harnessing state-of-the-art machine learning and computer vision technologies, the project is dedicated to identifying and anonymizing identifiable features such as faces, watermarks, and sensitive objects in both videos and images.

   * By integrating advanced tools including deep learning models, OpenCV, PyTorch, numpy, ffmpeg, face_recognition, and easyocr, the   project not only guarantees privacy but also upholds the integrity of visual content.

   * The project helps the users to protect their privacy by anonymizing the sensitive contents in the video or image such as faces, watermarks and sounds.

SecurAnon simplifies the process of safeguarding privacy in both images and videos. With its intuitive interface and powerful features, users can detect and blur faces, remove watermarks, and ensure compliance with privacy regulations, all while retaining full control over their media content.

The project offers three services :

    1. Auto Image Anonymization
        The auto image anonymization service of the secureanon automatically detects the presence of faces, personal identifiable information, text information in the image and provides an anonymized version of the image where the user can simply download the anonymized version of the image.

    2. Selective Image Anonymization
        The selective image anonymization service of the secureanon automatically detects the presence of faces and provides the facility to select the faces they want to anonymize. The user can download the selective anonymized version of the image.

    3. Video Anonymization
        The video anonymization service of the secureanon helps the user to upload the video and a refernce image the system automatically detects the presence of faces matching faces with the reference image in the video and also detects the presence of watermarks or any other text content in the video. The user can download the anonymized video after processing.

>> Frontend

    The frontend of the secureanon is developed using Nextjs and the elements Ui, Next ui are used to create attractive UI.
    
    Dependencies:

    - Nextjs                >> https://nextjs.org/docs
    - Element UI Elements   >> https://element.eleme.io/#/en-US 
    - Tailwind CSS          >> https://v2.tailwindcss.com/docs

>> Backend

    The backend of the secureanon is developed using the Python framework Flask which supports the various libraries required for the anonymization process.
    Dependencies:

    - Flask Flask-Cors   >> https://flask.palletsprojects.com/en/3.0.x/
    - pymongo            >> https://www.mongodb.com/docs/
    - dlib               >> https://dlib.net/python/index.html
    - opencv-python      >> https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
    - numpy              >> https://numpy.org/doc/
    - face_recognition   >> https://face-recognition.readthedocs.io/en/latest/readme.html
    - easyocr            >> https://github.com/JaidedAI/EasyOCR
    - Flask-JWT-Extended >> https://flask-jwt-extended.readthedocs.io/en/stable/
    - python-dotenv      >> https://pypi.org/project/python-dotenv/
    - bcrypt             >> https://pypi.org/project/bcrypt/

>> Database Description

    MongoDB is used as the database for this project. Initially the database named face needs to be created in the mongoDB.
    Refer mongoDB documentation for more information :
    >> https://www.mongodb.com/docs/

    Collections used in the mongoDB are :
    - Face
      * Anonymize :- Collection contains the details of the frame 
      * Image :- Collection containd the information of the auto image anonymization
      * Selective :- Collection contains the details of the selected image anonymization
      * User :- Collection contains the information about the users


NOTE: This project uses GPU support for various processing in the backend , if the system doesnot have a GPU support the system will use default CPU support instead of GPU. If the system have a GPU support the matching versions of CUDA Toolkit, Pytorch, CuDNN needs to be installed and the corresponding path must be defined.

>> Folder Structure
 
 - app : Routes, Authentication
    - dashboard
    - image
    - selective
    - Signin
    - Signup
 - components : UI of the System
    - Banner
    - Image
    - Navbar
    - Provide
    - Why
 - Frames : Contains the frames generated using opencv of the uploaded video 
 - model : Model used for the face detection from the images
 - output : Output files
 - Uploads : Contains the files uploaded by the users.

>> Backend file Structure

  app.py :- Main flask file.
  blurDB.py :- To blur the locstions on the frame.
  combineDB.py :- To combine the processed frames in the comparison folder based on the video id.
  compareDB.py :- To compare the the frames with the reference image.
  faceblurapp.py :- To blur the faces in the image.
  facedetector.py :- To detect the faces in the image.
  framesGPU.py :- To convert the video to frames and the frames are stored in the frames folder.
  imports.py :- Contains all required imports.


Getting Started

1. Create the project folder and install all the dependencies
    client:- >> npm install next
    server:- >> pip install flask
2. Run the following commands to run the client and server

    >> Client >> npm run dev
    >> Server >> python app.py
3. Open http://localhost:3000 in the browser window

    * Ensure that the  server is running using the desired port
      default port is http://127.0.0.1:5000
4. Use Sign In/SignUp option to create an account or login into your existing account.
5. After logging to the system choose desired services from the service section.

