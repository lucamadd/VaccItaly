from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import cross_origin, CORS
from flask_mail import Mail
import helper
import mysql.connector

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

# Obtain connection string information from the portal
config = {
  'host': read_settings.read('DB_SETTINGS', 'MYSQL_DATABASE_HOST'),
  'user': read_settings.read('DB_SETTINGS', 'MYSQL_DATABASE_USER'),
  'password': read_settings.read('DB_SETTINGS', 'MYSQL_DATABASE_PASSWORD'),
  'database': read_settings.read('DB_SETTINGS', 'MYSQL_DATABASE_DB'),
  'port': 3306,
  'ssl_ca': 'static/var/DigiCertGlobalRootG2.crt.pem', 
  'ssl_disabled': False
}

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
    try:
        data = request.form
        nome = data['nome']
        cognome = data['cognome']
        data_nascita = data['data_nascita']
        luogo_nascita = data['luogo_nascita']
        email = data['email']
        cod_fis = data['CF']
        password = data['password']
        print(nome, cognome, data_nascita, luogo_nascita, email, cod_fis, password)

        conn = mysql.connector.connect(**config)
        print("Connection established")

    except Exception as e:
        msg = e
        print(e)
        return f'<div id="message" class="ui error mini message" style="display: none;"><div class="header">\
            Si è verificato un errore nella registrazione</div>\
            <p>{msg}</p></div>'
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO db_utente VALUES (%s, %s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'), %s, %s)", 
            (cod_fis, email, nome, cognome, data_nascita, luogo_nascita, password))
            cursor.close()

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
            print(helper.send_registration_email(email, nome))
        except Exception as e:
            if 'primary' in str(e).lower():
                msg = 'Esiste già un utente con la stessa email o codice fiscale'
            else:
                msg = e
            return f'<div id="message" class="ui error mini message" style="display: none;">\
                <div class="header">Si è verificato un errore nella registrazione</div>\
            <p>{msg}</p></div>'
    return '<div id="message" class="ui success mini message" style="display: none;">\
        <div class="header">Registrazione effettuata con successo</div></div>'

@app.route('/log_user', methods = ['POST', 'GET', 'OPTIONS'])
def log_user():
    msg = '<div id="message" class="ui success mini message" style="display: none;">\
           <div class="header">Login effettuato con successo</div></div>'
    try:
        data = request.form
        email = data['email']
        password = data['password']
        print(email, password)

        conn = mysql.connector.connect(**config)
        print("Connection established")

    except Exception as e:
        msg = f'<div id="message" class="ui error mini message" style="display: none;"><div class="header">\
            Si è verificato un errore con la connessione al server</div>\
            <p>{e}</p></div>'
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM db_utente WHERE (email = %s AND password = %s) OR (cod_fis = %s AND password = %s)", 
            (email, password, email, password))
            result = cursor.fetchone()
            if cursor.rowcount == 1:
                session['loggedin'] = True
                session['nome'] = result[0]
            else:
                msg = '<div id="message" class="ui error mini message" style="display: none;">\
                <div class="header">Credenziali errate</div></div>'
            cursor.close()

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            msg = f'<div id="message" class="ui error mini message" style="display: none;">\
                <div class="header">Si è verificato un errore nella connessione al database</div>\
                <p>{e}</p></div>'
    return msg

@app.route('/login')
def login():
    if 'loggedin' in session:
        return render_template('profile.html', session = session)
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

if __name__ == '__main__':
    try:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.secret_key = '6724237ce80fbd35848335402ad3a074f8b3e37a' #sha1 of my day
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()