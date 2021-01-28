from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS

import os
import sys

if sys.platform.lower() == "win32": 
    os.system('color')

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/new_user', methods = ['POST', 'GET', 'OPTIONS'])
def new_user():
    data = request.form
    nome = data['nome']
    cognome = data['cognome']
    data_nascita = data['data_nascita']
    luogo_nascita = data['luogo_nascita']
    email = data['email']
    cod_fis = data['CF']
    password = data['password']
    #return json.dumps({'html':'<span>All fields good !!</span>'})
    print(nome, cognome, data_nascita, luogo_nascita, email, cod_fis, password)
    return 'ok'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')



if __name__ == '__main__':
    try:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()