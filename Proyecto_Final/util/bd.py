import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/misaelvalenzulamorales/Downloads/sie_final/db.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://credenciales-3ceef-default-rtdb.firebaseio.com/'
})

def initializationBD():
    ref = db.reference('/Credenciales')
    return ref