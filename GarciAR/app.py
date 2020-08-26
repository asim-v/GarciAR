

# imports for flask
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify,send_from_directory,make_response
from flask_mail import Mail, Message
#For File Management
from werkzeug.utils import secure_filename
from types import SimpleNamespace as Namespace
#Object Json Generator
from collections import namedtuple
import json
#Object Json Generator





# imports for firebase
from firebase_admin import credentials, firestore, auth
import firebase_admin.db as rtdb
import firebase_admin
import firebase
from google.cloud import storage
from google.oauth2 import service_account

import sys#DEBUG
import os#DEBUG

# custom lib
# import firebase_user_auth

# realtime communication
from flask_socketio import SocketIO, emit, send

import requests



#Cuenta de servicio con las claves de firestore para almacenar los modelos
CONFIG = {
  "type": "service_account",
  "project_id": "ggarciar",
  "private_key_id": "cbdf342cce267f7a350567c611451701bf83a841",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD1HEbk4h9jhwMp\nnHkUfI/v0JRdlalE/ZLBgGt5d2TIybzRfnDgIVogjfdXkRgHh+XKBTxla7bNcKxl\nPNUbeIdFoMQF0qm0pKxN3Zrmkza4fp/iRlPcNu1FbLiu6ZPDmPm6K/RIhe+NcCYD\n/ZHY0DRmxRocAmlRroIdqAMHST7ZUabLNCSQMzJxI0rWA/nU+UKyAzqynG4P9Ama\n+ENSbVobFVM3M9NqIcsCeRs7H1MNBA+DMSjnCY+UAeHm1qJyxITXdVdJYzx1TIv6\nNvQVf6VyrB5pVfoa04I3dbPK9IHjHywtU/QD9+BBVwE6powEvH7luKHWKdg1kZSI\nmYrwTmpXAgMBAAECggEAVrOP6DqMO9pwJfHxamu9RmkTch8UZxEDLmtMmQTAo72o\nirodF0r05HsTOOhcBZ3ujI1Zlc6KNRVcBduEzljOELUTYbPoz7tIL6rpthHw00YH\nLDUQSN8tAte4ZDa/S/r6qv4NRPILkI5RBCxXwMe1IX0rBSldM8V0xSS/HX6tOpVU\nIVgWEQ2j8J0Tomn+SLGzQw7u1Rx05KGEU3TDp+JvCAlSuP2aY3Dqcj/KwZYVRSED\nSGq6Lbcxl132/ATyAZZTXrNeNXiLHir0iNVMu5CrWoSvf1YRiT2rjkAwtCYTdhQN\nJN3kyTx3y4S4JEwyQOkxh7g4hpzA7Txfm6QwmdJ+AQKBgQD7BVBM5H1PduzuO12E\nCWQEQxa2Yx4PnSIrKQXVg8FeV28iQL+pQnAJu4GAnBDLfarpvywGPiHFQv9ypa5s\n+nS5zBqhxar4BTQouG/GwHe9T8Cd2RjLqYNCFCRLMpD6mS+N04ZfuXV8BOma3zdk\n/ZVPpabX+yauZ5eNszu3hmqT1wKBgQD5+PNgINBx+2p1ybKfMvfb2spOgh9xXUJd\nbe/3ELVQ1bCKkAPMJSPaYFHFO3YU8RkjMBv86OVTBfGZ4YDAc7EpAma8ZWjLh9vu\nKKVYkTM1HY11m8XRiLYf+0Gx34qlsx2LTWxh1Xu7dEcEl8UKCeuAyDYBylhmDjuc\n89j5qqgNgQKBgQDQztbBX8AtfgwRECj2UKl2MiiOh1zWOCvYI0PLHNKZm7nCkIHe\nVnnEXsmXJjuCSoMF9hS1DLIi2VyNDe1OkfjPJU1yDG/v6MQ+q02v0yLHw7PCmnjZ\n0aRyLzcRpnqbOxonrDE3J5rnE18PiWcXBypRGsbzGuROZ7XWFaYzQAkf+QKBgCBO\ncnXcB9STX8D1XmaA2dPKRRc8bf/iw677hGXz/NsDoxtlXXhG3IlepXLOKoauWkdX\n8mYPW4QNYpo2sMMusJjSPKDgolibqGrxSd1Wdr3Iof2vMjPQbWlYubbZYzvjGFBm\nozlJtAIYFw2a59ZSTeOI/KHimuYltMKmKUarLakBAoGBANN9lUO4ts0z6Mw2UsDw\nW1PF64TLjX4km7L8jQKM2549PgGewGRGj6PDxQ0wz2sDNDkLBexbke9JIea1JBUe\nBG99fMEHO+U9DLL7Ak9e0mu06gliwA9i4i9qD6TNU+hP1mxBrFafIM2BW9b/H9Sy\n6+PniMr9hKn97Pt34gBjr1cv\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-p4ipm@ggarciar.iam.gserviceaccount.com",
  "client_id": "105140238096513487290",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-p4ipm%40ggarciar.iam.gserviceaccount.com"
}


##EJEMPLOS
# posts = db.child("extraction").shallow().limit_to_first(5).get()  #Funciona
# posts = db.child("extraction").order_by_key().get()			   #Funciona
# posts = db.child("extraction").order_by_child("rt_OgFavCount").limit_to_first(5).get()#.val()
#SIRVE PARA PROBAR COMO GUARDAR FILES
# blob = bucket.blob('my-test-file.txt')
# blob.upload_from_string('this is test content!')
#SIRVE PARA PROBAR COMO GUARDAR FILES
##EJEMPLOS


#Sessions, init flask
app = Flask(__name__)
app.secret_key = b'\xbd\x93K)\xd3\xeeE_\xfb0\xa6\xab\xa5\xa9\x1a\t'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["FLASK_ENV"] = "development"
app.config["FLASK_DEBUG"] = "1"
socketio = SocketIO(app, cors_allowed_origins="*")




def dbinit():

  # initializes fb with bucket name
  cred = credentials.Certificate(CONFIG)
  default_app = firebase_admin.initialize_app(cred,{
      'storageBucket': 'ggarciar.appspot.com'
  })
  # configure buckets

  credentials = service_account.Credentials.from_service_account_info(CONFIG)
  client = storage.Client(project='fevici', credentials=credentials)

  bucket = client.get_bucket('ggarciar.appspot.com')

  #SIRVE PARA PROBAR COMO GUARDAR FILES
  # blob = bucket.blob('my-test-file.txt')
  # blob.upload_from_string('this is test content!')

  #Db referencias
  db = firestore.client()
  # users collection reference 
  users_coll = db.collection(u"users")
  # notes collection reference
  chats_coll = db.collection(u"notes")







@app.route('/')
def index():
  return render_template('index.html')

@app.route('/explorer')
def explorer():
  '''
    La idea es que el explorador esté viendo a un objeto 3d, y si se selecciona pueda devolver el id, 
    después hacer el routing a la ar con ese id.

    Ideas: Poder ver el mundo desde primera persona y tercera persona
  '''  
  return render_template('explorer/threejs-fps-controls-master/index.html')

@app.route('/ar/<id>')
def ar(id):
  '''
    Esta función al identificar el ar, renderiza la segunda app que consulta de la bd el modelo y detalles 
  '''
  return render_template('ar/index.html')
  
def save_file(file,uid = None):
    '''
        Dado objeto file, guardar en base de datos dada en proyectos
        Devuelve el id de donde ha sido guardado
    '''
    # gets the id of he old file to delete it
    user_doc = users_coll.document(session['id'])
    user_details = user_doc.get().to_dict()
    # return user_details   DEBUG
    try:
        project = user_details.get("project_file")['project_id']
        blob = bucket.blob(project) 
        blob.delete()
    except:pass
    # gets the old file and deletes it
    
    filename = ''.join([str(int(random.random()*1000000))])                    
    while filename in all_projects: filename = ''.join([str(int(random.random()*1000000))])                    
        

    blob = bucket.blob(filename) 
    blob.upload_from_file(file)    

    return filename

@app.route('/admin')
def admin():
  '''
  Basicamente hacer usuario y contraseña  (Super simple, incluso puede ser un 'a' == 'a') 
  e interfaz para subir:
   - Archivos 3d simples como sillas, mesas y xyz
    - Nombre, medidas y descripción
   - Mapas para el explorador
  '''
  return render_template('admin.html')










##Archivos Estáticos
@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('static/js', path)
@app.route('/img/<path:path>')
def send_img(path):
  return send_from_directory('static/images', path)
@app.route('/css/<path:path>')
def send_css(path):
  return send_from_directory('static/css', path)
@app.route('/fonts/<path:path>')
def send_fonts(path):
  return send_from_directory('static/fonts', path)
@app.route('/favicons/<path:path>')
def send_icons(path):
  return send_from_directory('static/favicons', path)





if (__name__ == "__main__"):
  dbinit()
  app.run(debug=True)
  #socketio.run(app, debug=True)  