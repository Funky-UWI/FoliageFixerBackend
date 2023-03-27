from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user

# from.index import index_views

from App.controllers import (
    create_user,
    authenticate, 
)
from App.controllers.scan import *


classify_views = Blueprint('classify_views', __name__, template_folder='../templates')

@classify_views.route(('/test_classify'), methods=['GET'])
def test():
    return 'works', 200


@classify_views.route('/classify', methods=['POST'])
# @jwt_required()
def upload_scan():
   
    data = request.json

    # Get the image file from the request
    image_file = request.files['image']

    # Run the image through the classification model to get the prediction

    classification = "healthy"
    severity = 45

    # Create a new Scan object and set its image attribute to the uploaded file
    scan = create_scan(image=image_file.read(),classification=classification, severity=severity,user_id=data["user_id"])
    if scan:
        return jsonify(scan.toJSON()), 201
    return jsonify({"error"}), 400



    

