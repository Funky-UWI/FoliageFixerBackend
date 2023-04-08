from flask import jsonify
from App.models import Classification
from App.database import db

def create_classification(name):
    classification = Classification(name)
    try:
        db.session.add(classification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return 'Classification created.'

# def update_classification_name(id, new_name):
#     classification = Classification.query.get(id)
#     classification.classification = new_name
#     db.session.update(classification)
#     db.session.commit()

def get_classification_id_by_name(name):
    classification = Classification.query.filter_by(classification=name).first()
    return classification.id

def get_all_classifications():
    return Classification.query.all()

def get_all_classifications_json():
    classifications = Classification.query.all()
    if not classifications:
        return []
    classifications = [classification.get_json() for classification in classifications]
    return classifications