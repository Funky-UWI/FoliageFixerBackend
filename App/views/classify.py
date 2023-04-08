from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from PIL import Image
import pyrebase
import base64
import io
import os
import numpy as np
from json import loads
#importing firebase auth libraries
import pyrebase
import firebase_admin
from firebase_admin import auth

# import firebase app
import App.firebase as fb
# fb_admin=fb.connect_admin()
fb_admin = fb.get_admin()

from App.controllers import (
    create_user,
    authenticate, 
)
from App.controllers.scan import *
from App.controllers.classification import *
from App.controllers.disease_Solution import *
from App.controllers.ml_models import *

classify_views = Blueprint('classify_views', __name__, template_folder='../templates')

@classify_views.route(('/test_classify'), methods=['GET'])
def test():
    return 'works', 200


# INITIALIZE MODELS
# segmentation_model = get_segmentation_model()

@classify_views.route('/classify', methods=['POST'])
def upload_scan():

    #getting token from the request headers
    id_token= request.headers.get('authorization')
    print(id_token)
    try:
        decoded_token=auth.verify_id_token(id_token)

        # getting user id from the token
        user_id= decoded_token['uid']
   
        data = request.form

        # Get the image file from the request
        image_file = request.files['image']

        image_data = image_file.read()

        '''
        Classification with models stored locally
        ** do not delete
        '''
        # # Run the image through the classification model to get the prediction
        # # step 1 load image as tensor
        # image = FileStorage_to_Tensor(image_data)
        # print(type(image))
        # # step 2 segment image
        # leaf, disease = segmentation_model(image.unsqueeze(0))
        # # step 3 compute severity
        # severity = compute_severity(leaf.squeeze(0), disease.squeeze(0))
        # print('severity: ', severity)
        # # step 4 classify
        # classification_model = get_classification_model()
        # outputs = classification_model(disease)
        # classification = get_classification(outputs)

        '''
        classification with azure function
        '''
        response = request_classification_from_azure(image_bytes=image_data)
        if response.status_code == 200:
            model_prediction = loads(response.text)
        else:
            return "Error uploading file", response.status_code

        classification = model_prediction['classification']
        severity = model_prediction['severity']

        # step 5 get classification id
        classification_ID= get_classification_id_by_name(classification)
        # step 6 get solutions for the classification ID
        solutions = get_solutions_by_classification(classification_ID)

        print(type(image_file), type(image_data))

        # save image to firebase
        response = fb.save_scan_image(image_bytes=image_data)
        path = response['name']
        downloadTokens = response['downloadTokens']
        image_url = fb.get_image_url(path, downloadTokens)
        # create scan object
        scan=create_scan(image=image_url, classification_id=classification_ID, severity=severity, user_id=user_id)

        return jsonify({
            "severity": severity,
            "classification": classification,
            "classification_id": classification_ID,
            "solutions": solutions,
            "image_url": scan.image
        })
    # except auth.AuthError:
    except (auth.ExpiredIdTokenError, auth.ExpiredSessionCookieError, auth.InvalidIdTokenError, auth.InvalidSessionCookieError) as E:
        print(E)
        return jsonify({'error': E.__str__()}), 401
    except Exception as E:
        print(E)
        # if the token is invalid or authentication fails, return an error message
        # return jsonify({'error': 'Invalid token or authentication failed'}), 401
        return jsonify({
            'error': E.__str__()
        }), 500


@classify_views.route('/recent',methods=['GET'])
def get_recent_scans():
    #getting token from the request headers
    id_token= request.headers.get('authorization')
    try:
        decoded_token=auth.verify_id_token(id_token)

        # getting user id from the token
        user_id= decoded_token['uid']
   

        # params = request.args
        # user_id = params.get('user_id')
        # print(user_id)
        if user_id:
            return get_scans_by_user_json(user_id)
        else:
            return get_all_scans_json()

    except (auth.ExpiredIdTokenError, auth.ExpiredSessionCookieError, auth.InvalidIdTokenError, auth.InvalidSessionCookieError) as E:
        print(E)
        return jsonify({'error': E.__str__()}), 401
    except Exception as E:
        print(E)
        # if the token is invalid or authentication fails, return an error message
        # return jsonify({'error': 'Invalid token or authentication failed'}), 401
        return jsonify({
            'error': E.__str__()
        }), 500

@classify_views.route('/azure', methods=['POST'])
def azure():
    image_file = request.files['image']
    response = request_classification_from_azure(image_bytes=image_file.read())
    if response.status_code == 200:
        return loads(response.text), 200
    else:
        return "Error uploading file", response.status_code



    

@classify_views.route('/loginn', methods=['POST'])
def login():
    try:
        # get the user's email and password from the request body
        email = request.form.get('email')
        password = request.form.get('password')

        print(email)

        # authenticate the user using the Firebase Authentication REST API
        response = requests.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + "AIzaSyBbbVpZeszVu5jT1hFVCuSvXgTz2hoWYRg",
            json={
                'email': email,
                'password': password,
                'returnSecureToken': True
            }
        )

        # if the authentication was successful, return the custom token
        if response.status_code == 200:
            return jsonify({'token': response.json()['idToken']})

        # if the authentication failed, return an error message
        else:
            return jsonify({'error': 'Authentication failed'}), response.status_code
    except Exception as E:
        print(E)
        # if the token is invalid or authentication fails, return an error message
        # return jsonify({'error': 'Invalid token or authentication failed'}), 401
        return jsonify({
            'error': E.__str__()
        }), 500
    

@classify_views.route('/adduser', methods=['POST'])
def add_user_view():
    id_token = request.headers.get('authorization')
    try:
        decoded_token=auth.verify_id_token(id_token)
    except Exception as e:
        print(e)
        return jsonify(e.__str__()), 401
    
    uid = decoded_token['uid']
    print(decoded_token)
    try:
        user = create_user(uid)
    except Exception as e:
        return jsonify(e.__str__()), 400
    return user.get_json()