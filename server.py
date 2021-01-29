from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS
import mysql.connector
from mysql.connector import errorcode

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

# Obtain connection string information from the portal
config = {
  'host': read_settings.read('MYSQL_DATABASE_HOST'),
  'user': read_settings.read('MYSQL_DATABASE_USER'),
  'password': read_settings.read('MYSQL_DATABASE_PASSWORD'),
  'database': read_settings.read('MYSQL_DATABASE_DB'),
  'port': 3306,
  'ssl_ca': 'static/var/DigiCertGlobalRootG2.crt.pem', 
  'ssl_disabled': False
}
# MySQL configurations
#app.config['MYSQL_USER'] = read_settings.read('MYSQL_DATABASE_USER')
#app.config['MYSQL_PASSWORD'] = read_settings.read('MYSQL_DATABASE_PASSWORD')
#app.config['MYSQL_DB'] = read_settings.read('MYSQL_DATABASE_DB')
#app.config['MYSQL_HOST'] = read_settings.read('MYSQL_DATABASE_HOST')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

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
        return f'<div id="message" class="ui error mini message" style="display: none;"><div class="header">Si è verificato un errore nella registrazione</div>\
            <p>{msg}</p></div>'
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO db_utente VALUES (%s, %s, %s, %s, STR_TO_DATE(%s,'%d/%m/%Y'), %s, %s)", (cod_fis, email, nome, cognome, data_nascita, luogo_nascita, password))
            cursor.close()

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            if 'primary' in str(e).lower():
                msg = 'Esiste già un utente con la stessa email o codice fiscale'
            else:
                msg = e
            return f'<div id="message" class="ui error mini message" style="display: none;"><div class="header">Si è verificato un errore nella registrazione</div>\
            <p>{msg}</p></div>'
    return '<div id="message" class="ui success mini message" style="display: none;"><div class="header">Registrazione effettuata con successo</div></div>'

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