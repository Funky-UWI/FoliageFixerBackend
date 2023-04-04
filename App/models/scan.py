from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
import base64

    
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    # classification = db.Column(db.String(50), nullable=False)
    classification_id = db.Column(db.Integer,db.ForeignKey('classification.id'),nullable=False)
    classification = db.relationship('Classification')
    severity = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, image, classification_id, severity, user_id):
        self.image=image
        self.classification_id=classification_id
        self.severity=severity
        self.user_id=user_id 

    def toJSON(self):
        return{
            'id': self.id,
            'classification': self.classification.get_json(),
            'severity': self.severity,
            'user_id': self.user_id,
            # 'image': base64.b64encode(bytes(str(self.image), encoding='utf-8')).decode('utf-8')
            'image': self.image
        } 

    def __repr__(self):
        return f"<Scan {self.id}>"

