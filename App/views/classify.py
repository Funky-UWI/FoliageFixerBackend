from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

# from.index import index_views

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
segmentation_model = get_segmentation_model()

@classify_views.route('/classify', methods=['POST'])
def upload_scan():
   
    data = request.form

    # Get the image file from the request
    image_file = request.files['image']

    # Run the image through the classification model to get the prediction
    # step 1 load image as tensor
    image = FileStorage_to_Tensor(image_file)
    print(type(image))
    # step 2 segment image
    leaf, disease = segmentation_model(image.unsqueeze(0))
    # step 3 compute severity
    severity = compute_severity(leaf.squeeze(0), disease.squeeze(0))
    print('severity: ', severity)
    # step 4 classify
    classification_model = get_classification_model()
    outputs = classification_model(disease)
    classification = get_classification(outputs)
    # step 5 get classification id
    classification_ID= get_classification_id_by_name(classification)
    # step 6 get solutions for the classification ID
    solutions = get_all_solutions_json()

    return jsonify({
        "severity": severity,
        "classification": classification,
        "classification_id": classification_ID,
        "solutions": solutions
    })


@classify_views.route('/recent',methods=['GET'])
def get_recent_scans():
    scans = get_all_scans_json()
    return jsonify(scans)




    

