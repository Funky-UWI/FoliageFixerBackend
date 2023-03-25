from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class DiseaseSolution(db.Model):
    __tablename__ = 'disease_Solution'

    id = db.Column(db.Integer, primary_key=True)
    # classification = db.Column(db.String(50), nullable=False)
    classification_id = db.Column(db.Integer,db.ForeignKey('classification.id'),nullable=False)
    classification = db.relationship('Classification')
    solution = db.Column(db.String(500), nullable=False)

    def __init__(self, classification_id, solution):
        self.classification_id = classification_id
        self.solution = solution

    def get_json(self):
        return {
            'classification': self.classification.get_json(),
            'solution': self.solution
        }

   
