import pyrebase
import uuid
import firebase_admin 
from firebase_admin import auth, credentials
from cryptography.fernet import Fernet
from os import unlink

firebase = None
fb_admin=None

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

def connect_admin():
    priv_key_path = 'priv_key.json'
    # cred = credentials.Certificate('App/foliagefixer-firebase-adminsdk-y8row-36eb6d6b41.json') 
    with open('decryption_key.key', 'rb') as file:
        key = file.read()
    print(key)
    fernet = Fernet(key)
    with open('encrypted.json', 'rb') as file:
        token = file.read()
    print(token)
    priv_key = fernet.decrypt(token)
    print(priv_key)
    with open(priv_key_path, 'wb') as file:
        file.write(priv_key)
    cred = credentials.Certificate(priv_key_path)
    # delete file
    # unlink(priv_key_path)
    global fb_admin
    fb_admin = firebase_admin.initialize_app(cred) 
    return fb_admin

def get_admin():
    return fb_admin
