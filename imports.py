import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory,json,g
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
import framesGPU
import connection
import audioDB
from bson.json_util import dumps,loads 
import bcrypt
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,get_jwt_identity,jwt_required
import jwt
import datetime
from dotenv import load_dotenv
from faceblurapp import FaceBlurApp
from facedetecterapp import FaceDetector
import easyocr
from datetime import timedelta
from flask import session
from flask_login import LoginManager, UserMixin, login_user, current_user
from moviepy.editor import *
import sendemail
from flask_mail import *