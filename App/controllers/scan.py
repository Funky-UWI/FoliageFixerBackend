from App.models import Scan
from App.database import db 

def create_scan(image,classification_id,severity, user_id):
    try:
        scan=Scan(image=image, classification_id=classification_id, severity=severity, user_id=user_id)
        db.session.add(scan)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return scan

def get_all_scans():
    return Scan.query.all()

def get_all_scans_json():
    scans= Scan.query.all()
    return[ scan.toJson() for scan in scans]

def get_scans_by_user(user_id):
    return Scan.query.filter_by(user_id=user_id)

def get_scans_by_user_json(user_id):
    scans = Scan.query.filter_by(user_id=user_id)
    return [scan.toJSON() for scan in scans]
