from App.models import Scan
from App.database import db 

def create_scan(image,classification,severity, strategy_id, user_id):
    scan=Scan(image=image, classification=classification, severity=severity, user_id=user_id)
    db.session.add(scan)
    db.session.commit()
    return scan

def get_all_scans():
    return Scan.query.all()

def get_all_scans_json():
    scans= Scan.query.all()
    if scans:
        return[ scans.toJson() for scans in scans]

def get_scan_by_user(user_id):
    return Scan.query.filter_by(user_id=user_id).first()
