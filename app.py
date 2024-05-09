from imports import *

# Connect to MongoDB (replace with your connection details)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["face"]  # Replace with your database name
frames_collection = db["Image"]  # Replace with your collection name
selective_collection=db["Selective"]
user_collection=db["User"]
otp_collection=db["Otp"] # Replace with your collection name
app = Flask(__name__)
CORS(app)
jt=JWTManager(app)
current_user='don@gmail.com'
# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
mail=Mail(app)

app.config['JWT_SECRET_KEY']=os.environ.get('JWT_SECRET_KEY')
exp=app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=0)
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

def load_user(email): 
    data=user_collection.find_one({'email': email})
    if data:
        return data
    else:
        return 201

def verification():
    print(app.config['JWT_SECRET_KEY'])
    auth_header = request.headers.get('Authorization')
    print("authentication", auth_header)
    if not auth_header or not auth_header.startswith('Bearer '):
        print("no jet token is provided")
        return jsonify({'error': 'No JWT token provided'}), 401

    token = auth_header.split()[1]
    print(token)
    decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms='HS256')
    print("decoded_token", decoded_token)
    user_identity = decoded_token['sub']
    print("useridentity", user_identity)
    ver = load_user(user_identity)
    return ver, user_identity
@app.route('/api/file', methods=['POST'])

def upload_file():

    ver,user_identity=verification()
    print("file upload",user_identity)
    if ver:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_identity+timestamp+file.filename)
        file.save(file_path)

        blur_factor = int(request.form.get('blur_factor', 3))  # Default blur factor is 3
        blur_all_faces = request.form.get('blur_all_faces', 'true').lower() == 'true'
        face_blurrer = FaceBlurApp()
        output_filename = 'blurred_' +user_identity+timestamp+ file.filename
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


@app.route('/api/face', methods=['POST'])
def uploads_file():
    ver,user_identity=verification()
    if ver:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        f1=request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_identity+timestamp+file.filename)
        
        file.save(file_path)
        print("f1",f1.filename)
        static_path=os.path.join(app.config['STATIC_FOLDER'],user_identity+timestamp+f1.filename)
        shutil.copy(file_path,static_path)
        face_detector = FaceDetector()
        detected_faces = face_detector.detect_faces(file_path)
        print('face_detector detected',detected_faces)
        # Convert int32 values to Python integers for JSON serialization
        for face_list in detected_faces:
                face_list['coordinates'] = [int(coord) for coord in face_list['coordinates']]

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
            sigma = 30 * math.log(blur_factor + 5, 2)  # Scale blur factor (adjust multiplier if needed)
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
        ver,user_identity=verification()
        if ver:
            if 'file' not in request.files:
                return jsonify({'error':'No file part'}), 400
            file=request.files['file']
            if file.filename=='':
                return jsonify({'error':'No file is selected'}), 400
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            file_path=os.path.join(app.config['UPLOAD_FOLDER'],user_identity+timestamp+file.filename)
            file.save(file_path)
            output_folder = os.path.join("frames")
            video_id =user_identity+timestamp  # Set the video ID here
            framesGPU.save_frames_to_db(file_path,output_folder,video_id,user_identity)
            return jsonify({'file_path':file_path,'video_id':video_id})
    
@app.route('/api/reference', methods=['POST'])
def reference():
    ver,user_identity=verification()
    if ver:
    # Check if 'file' exists in request.files
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        # Get the file from the request
        file = request.files['file']
        
        # Check if a file was provided
        if file.filename == '':
            return jsonify({'error': 'No file is selected'}), 400
        
        # Save the file to the upload folder
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_identity+timestamp+file.filename)
        file.save(file_path)
        
        # Get other data from the request body
        video_path = request.form['video_path']
        video_id = request.form['video_id']
        
        audioDB.extract_audio(video_path,video_id)
        compareDB.save_frames_to_db(video_path, video_id, file_path)
        blurDB.blur_and_save_frames(video_path,video_id)
        output_file=combineDB.combine_frames_from_db(user_identity,video_id)
        # combined_video=audioDB.combine_audio(video_id,output_file)
      
        return jsonify({'success': 'Video has been compared.','output': output_file})
   

@app.route('/api/register', methods=['POST'])
def register():
    email = request.form.get('email')
    check = user_collection.find_one({'email': email})
    if check:
        return jsonify({'msg': 'Username already registered', 'status_code': 500})
    else:
        old = otp_collection.find_one({'email': email})
        otp = 102506 #sendemail.verify(email)
        print(otp)
        current_timestamp = datetime.datetime.now().timestamp()
        if old:
            con = otp_collection.update_one({'email': email}, {'$set': {'otp': otp, 'timestamp': current_timestamp}})
            if con:
                return jsonify({'msg': 'OTP send successfully', 'email': email, 'otp': otp, 'status_code': 201}), 201
            else:
                return jsonify({'msg': 'Registration Failure', 'status_code': 500}), 500
        else:
            frames_data = {
                'email': email,
                'otp': otp,
                'timestamp': current_timestamp
            }

        con = otp_collection.insert_one(frames_data)
        if con:
            return jsonify({'msg': 'OTP send successfully', 'email': email, 'otp': otp, 'status_code': 201}), 201
        else:
            return jsonify({'msg': 'Registration Failure', 'status_code': 500}), 500


import datetime

@app.route('/api/verify', methods=['POST'])
def verify():
    email = request.form.get('email')
    otp = request.form.get('otp')
    password = request.form.get('password')
    
    # Check OTP from the otp_collection
    check = otp_collection.find_one({'email': email})
    
    if check and int(otp) == check['otp']:
        # Check if OTP is within the valid time frame (10 minutes)
        otp_timestamp = check.get('timestamp', 0)
        current_timestamp = datetime.datetime.now().timestamp()
        if current_timestamp - otp_timestamp <= 600:  # 600 seconds = 10 minutes
            hashed = connection.register(password)
            frames_data = {
                'email': email,
                'password': hashed,
            }
            con = user_collection.insert_one(frames_data)
            
            if con:
                otp_collection.delete_one({'email':email})
                return jsonify({'msg': 'Registration successfully', 'status_code': 201}), 201
            else:
                return jsonify({'msg': 'Registration Failure', 'status_code': 500}), 500
        else:
            return jsonify({'msg': 'OTP expired', 'status_code': 401}), 401
    else:
        return jsonify({'msg': 'Invalid OTP', 'status_code': 401}), 401
@jwt_required
def curr():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200   

@app.route('/api/login',methods=['POST'])
def reg():
    email=request.form.get('email')
    passd=request.form.get('passw')
    print(email,passd)
    data=user_collection.find_one({'email':email}) 
    if data:
        hashed=data.get('password')
        pa=passd.encode('utf8')
    if bcrypt.checkpw(pa,hashed):
        #access token creation
        access_token=create_access_token(identity=email)
        print(app.config['JWT_SECRET_KEY'])
        
        return jsonify({'msg':'Login successful','token':access_token})
    else:
        return jsonify({'msg':'Invalid password'})
    
    
@app.route('/api/protected', methods=['GET'])
@jwt_required()  # Ensure JWT token is present and valid
def protected():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200    


    
if __name__ == '__main__':
    app.run(debug=True)