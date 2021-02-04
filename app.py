from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import cross_origin, CORS
from flask_mail import Mail
import helper
import db_functions as db
import traceback


import read_settings
import os
import sys

if sys.platform.lower() == "win32": 
    os.system('color')


app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

mail = Mail(app) # instantiate the mail class 

   
# configuration of mail 
app.config['MAIL_SERVER']= read_settings.read('EMAIL_SETTINGS', 'MAIL_SERVER')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = read_settings.read('EMAIL_SETTINGS', 'MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = read_settings.read('EMAIL_SETTINGS', 'MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', session = session)

@app.route('/register')
def register():
    if 'loggedin' in session:
        return render_template('profile.html', session = session)
    return render_template('register.html', session = session)

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
    print(nome, cognome, data_nascita, luogo_nascita, email, cod_fis, password)
        
    return db.new_user(nome, cognome, data_nascita, luogo_nascita, email, cod_fis, password)

@app.route('/log_user', methods = ['POST', 'GET', 'OPTIONS'])
def log_user():
    data = request.form
    email = data['email']
    password = data['password']
    print(email, password)

    return db.log_user(email, password, session)

    
    

@app.route('/login')
def login():
    if 'loggedin' in session:
        return render_template('profile.html', session = session)
    return render_template('login.html', session = session)

@app.route('/reserve')
def reserve():
    if 'loggedin' in session:
        return render_template('reserve.html', session = session)
    return render_template('login.html', session = session)

@app.route('/terms')
def terms():
    return render_template('terms.html', session = session)

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', session = session)
    return redirect(url_for('login'))

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('nome', None) 
    return redirect(url_for('login')) 

@app.route('/get_elenco_comuni', methods = ['POST', 'OPTIONS']) 
def get_elenco_comuni():
    if 'loggedin' in session:
        data = request.form
        regione = data['regione']
        return helper.get_elenco_comuni(regione)
    return redirect(url_for('index'))

@app.route('/get_numero_vaccini', methods = ['GET', 'POST', 'OPTIONS']) 
def get_numero_vaccini():
    if 'loggedin' in session:
        data = request.form
        regione = data['regione']
        return helper.get_numero_vaccini(regione)
    return redirect(url_for('index'))

@app.route('/edit_vaccini', methods = ['GET', 'POST', 'OPTIONS']) 
def edit_vaccini():
    return ''    

@app.errorhandler(500)
def internal_server_error(e):
    #set the 500 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    helper.send_bug_report_msg(session, type(e), str(e), traceback.format_exc())
    return render_template('error.html')

if __name__ == '__main__':
    try:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.secret_key = '6724237ce80fbd35848335402ad3a074f8b3e37a' #sha1 of my day
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()