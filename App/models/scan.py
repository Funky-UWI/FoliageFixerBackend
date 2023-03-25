from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

    
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    # classification = db.Column(db.String(50), nullable=False)
    classification_id = db.Column(db.Integer,db.ForeignKey('classification.id'),nullable=False)
    classification = db.relationship('Classification')
    severity = db.Column(db.Float, nullable=False)
    # management_strategy = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, image, classification_id, severity, management_strategy,user_id):
        self.image=image
        self.classification_id=classification_id
        self.severity=severity
        self.management_strategy=management_strategy
        self.user_id=user_id 

    def __repr__(self):
        return f"<Scan {self.id}>"

