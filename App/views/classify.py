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


classify_views = Blueprint('classify_views', __name__, template_folder='../templates')

@classify_views.route(('/test_classify'), methods=['GET'])
def test():
    return 'works', 200


@classify_views.route('/classify', methods=['POST'])
# @jwt_required()
def upload_scan():
   
    data = request.form

    # Get the image file from the request
    image_file = request.files['image']

    # Run the image through the classification model to get the prediction



    # test data for now
    classification = "healthy"
    severity = 45

    classification_ID= get_classification_id_by_name(classification)
    # solutions= get_all_solutions_json()

    # Create a new Scan object and set its image attribute to the uploaded file
    scan = create_scan(image=image_file.read(),classification=classification_ID, severity=severity,user_id=data["user_id"])
    if scan:
        return jsonify(scan.toJSON()), 201
    return jsonify({"error"}), 400


@classify_views.route('/recent',method=['GET'])
def get_recent_scans():
    scans = get_all_scans_json()
    return jsonify(scans)




    

