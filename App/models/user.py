from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    scans = db.relationship('Scan', backref='user', lazy=True)

    def __init__(self, id):
        self.id = id

    def get_json(self):
        return{
            'id': self.id,
            'scans': self.scans
        }

