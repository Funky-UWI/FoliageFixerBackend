import pyrebase
import uuid
import firebase_admin 
from firebase_admin import auth

firebase = None

config = {
    'apiKey': "AIzaSyBbbVpZeszVu5jT1hFVCuSvXgTz2hoWYRg",
    'authDomain': "foliagefixer.firebaseapp.com",
    'projectId': "foliagefixer",
    'storageBucket': "foliagefixer.appspot.com",
    'messagingSenderId': "46934237736",
    'appId': "1:46934237736:web:013ef075fa1e21b5418b1d",
    'measurementId': "G-VG6JB5GLG6",
    'databaseURL': ''
}

def create_firebase(app):
    # set config variables
    # app.config['apiKey'] = "AIzaSyBbbVpZeszVu5jT1hFVCuSvXgTz2hoWYRg",
    # app.config['authDomain'] = "foliagefixer.firebaseapp.com",
    # app.config['projectId'] = "foliagefixer",
    # app.config['storageBucket'] = "foliagefixer.appspot.com",
    # app.config['messagingSenderId'] = "46934237736",
    # app.config['appId'] = "1:46934237736:web:013ef075fa1e21b5418b1d",
    # app.config['measurementId'] = "G-VG6JB5GLG6"
    # app.config['databaseURL'] = ''

    # init firebase app
    global firebase 
    firebase = pyrebase.initialize_app(config)
    return firebase

def get_firebase():
    return firebase

def save_scan_image(image_bytes):
    filename = uuid.uuid4().hex
    storage = firebase.storage()
    response = storage.child(f'images/{filename}').put(image_bytes)
    return response

def get_image_url(path, downloadTokens):
    storage =firebase.storage()
    url = storage.child(path).get_url(downloadTokens)
    return url