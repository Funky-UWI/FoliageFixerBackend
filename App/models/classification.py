from App.database import db

class Classification(db.Model):
    __tablename__ = 'classification'

    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(50), nullable=False, unique=True)


    def __init__(self, classification):
        self.classification = classification

    def get_json(self):
        return{
            'id': self.id,
            'classification': self.classification
        }