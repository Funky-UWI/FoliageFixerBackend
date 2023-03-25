from flask import jsonify
from App.models import Classification
from App.database import db

def create_classification(name):
    classification = Classification(name)
    db.session.add(classification)
    db.session.commit()
    return 'Classification created.'

def get_classification_id_by_name(name):
    classification = Classification.query.filter_by(classification=name).first()

def get_all_classifications():
    return Classification.query.all()

def get_all_classifications_json():
    classifications = Classification.query.all()
    if not classifications:
        return []
    classifications = [classification.get_json() for classification in classifications]
    return classifications