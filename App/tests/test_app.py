import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user
)

# from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):
    id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    def test_new_user(self):
        user = User(self.id)
        assert user.id == self.id

    def test_to_json(self):
        user = User(self.id)
        json = user.get_json()
        self.assertDictEqual(json, {
            'id': self.id,
            'scans': []
        })

class ClassificationUnitTests(unittest.TestCase):
    classifications = [
        "Healthy"
        "Bacterial Spot"
        "Early Blight"
        "Late Blight"
        "Leaf Mold"
        "Septoria Leaf Spot"
        "Tomato Mosaic Virus"
        "Yellow Leaf Curl Virus"
    ]

    def test_new_classification(self):
        c = Classification(self.classifications[0])
        assert c.classification == self.classifications[0]

    def test_get_json(self):
        classification = Classification(self.classifications[0])
        self.assertDictEqual(classification.get_json(), {
            'id': None,
            'classification': self.classifications[0]
        })

    def test_all_classifications(self):
        classifications = []
        for c in self.classifications:
            classification = Classification(c)
            classifications.append(classification)
        self.assertListEqual(
            [classification.get_json() for classification in classifications],
            [{
                'id': None,
                'classification': classification
            } for classification in self.classifications]
            )

class ScanUnitTests(unittest.TestCase):
    image = "https://firebasestorage.googleapis.com/v0/b/foliagefixer.appspot.com/o/images%2F257394c877d64a4499b2bd19153a9b82?alt=media&token=329e53e1-5a5a-47be-a7c5-d253a7be2453"
    severity = 0.50505050505
    classification_id = 1
    user_id = 1

    def test_new_scan(self):
        scan = Scan(self.image, self.classification_id, self.severity, self.user_id)
        assert (scan.image == self.image and 
        scan.classification_id == self.classification_id and
        scan.severity == self.severity and
        scan.user_id == self.user_id and 
        scan.classification == None)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert authenticate("bob", "bobpass") != None

# class UsersIntegrationTests(unittest.TestCase):

#     def test_create_user(self):
#         user = create_user("rick", "bobpass")
#         assert user.username == "rick"

#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

#     # Tests data changes in the database
#     def test_update_user(self):
#         update_user(1, "ronnie")
#         user = get_user(1)
#         assert user.username == "ronnie"
