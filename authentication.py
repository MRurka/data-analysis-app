import pyrebase
from creds import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()