from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from PIL import Image
import base64
import io, os

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
    solutions = get_solutions_by_classification(classification_ID)

    #saving the image to the database as a String using base64 encoding
    image_data=image_file.read()
    img = Image.open(io.BytesIO(image_data))
    # Resize the image to a fixed size
    img = img.resize((224, 224))
    # Convert the image to a grayscale array
    img_array = np.array(img.convert('L'))
    # Convert the image array to a Base64-encoded string
    image_str = base64.b64encode(img_array).decode('utf-8')

    scan=create_scan(image=image_str, classification=classification_ID, severity=severity, user_id=data["user_id"])
    # if scan:
    #     return jsonify(scan.toJSON()), 201
    # return jsonify({"error"}), 400

    return jsonify({
        "severity": severity,
        "classification": classification,
        "classification_id": classification_ID,
        "solutions": solutions
    })


@classify_views.route('/recent',methods=['GET'])
def get_recent_scans():
    params = request.args
    user_id = params.get('user_id')
    print(user_id)
    if user_id:
        return get_scans_by_user_json(user_id)
    else:
        return get_all_scans_json()




    

