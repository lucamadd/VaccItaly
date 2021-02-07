from flask import Flask, render_template, request, session, redirect, url_for, jsonify
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
        if session['cod_fis'] == 'global_admin':                   #admin, non può prenotare
            return render_template('reserve.html', session = session, reservation='admin')
        reservation = db.check_prenotazione(session['email'])
        if reservation == 1:    #già prenotato
            return render_template('reserve.html', session = session, reservation=True)
        elif reservation == 0:  #deve ancora prenotare
            return render_template('reserve.html', session = session, reservation=False)
    return render_template('login.html', session = session)

@app.route('/terms')
def terms():
    return render_template('terms.html', session = session)


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        if session['cod_fis'] == 'global_admin':                   #admin, non può prenotare
            return render_template('profile.html', session = session, reservation='admin')
        reservation = db.check_prenotazione(session['email'])
        if reservation == 1:    #già prenotato
            return render_template('profile.html', session = session, reservation=True)
        elif reservation == 0:  #deve ancora prenotare
            return render_template('profile.html', session = session, reservation=False)
    return redirect(url_for('login'))

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('nome', None) 
    session.pop('cod_fis', None)
    session.pop('email', None)
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
        return jsonify(db.get_numero_vaccini(regione))
    return redirect(url_for('index'))

@app.route('/get_totale_vaccini', methods = ['GET', 'POST', 'OPTIONS']) 
def get_totale_vaccini():
    vaccini = []
    vaccini = db.get_totale_vaccini()
    return jsonify(vaccini)

@app.route('/edit_vaccini', methods = ['GET', 'POST', 'OPTIONS']) 
def edit_vaccini():
    data = request.form
    regione = data['regione']
    num_vaccini = data['num_vaccini']
    return db.edit_vaccini(regione, num_vaccini)   

@app.route('/add_prenotazione', methods = ['GET', 'POST', 'OPTIONS']) 
def add_prenotazione():
    data = request.form
    regione = data['regione']
    asl = data['asl'].strip()
    data_appuntamento = data['data_appuntamento']
    id_user = session['email']
    print(f'id_user: {id_user}\n\
            regione: {regione}\n\
                asl: {asl}\n\
               data: {data_appuntamento}')
    return db.new_prenotazione(id_user, regione, asl, data_appuntamento)

@app.route('/check_prenotazione', methods = ['GET', 'POST', 'OPTIONS']) 
def check_prenotazione():
    id_user = session['email']
    return db.check_prenotazione(id_user)

@app.route('/get_num_prenotazioni', methods = ['GET', 'POST', 'OPTIONS'])
def get_num_prenotazioni():
    if 'loggedin' in session:
        if session['cod_fis'] == 'global_admin':
            prenotazioni = {}
            prenotazioni = db.get_prenotazioni()
            return jsonify(prenotazioni)
    return str(False)

@app.route('/get_dettagli_utente', methods = ['GET', 'POST', 'OPTIONS']) 
def get_dettagli_utente():
    id_user = session['email']
    return jsonify(db.get_dettagli_utente(id_user))

@app.route('/delete_account', methods = ['GET', 'POST', 'OPTIONS']) 
def delete_account():
    if 'loggedin' in session:
        data = request.form
        email = data['email']
        if(db.delete_account(email)):
            session.pop('loggedin', None) 
            session.pop('nome', None) 
            session.pop('cod_fis', None)
            session.pop('email', None)
            return jsonify({
                'result': url_for('index', deleted=True),
                'deleted': True
                })
        else:
            return jsonify({
                'result': url_for('profile', deleted=False),
                'deleted': False
                })
    return redirect(url_for('index'))

@app.route('/check_date', methods = ['GET', 'POST', 'OPTIONS']) 
def check_date():
    date_non_disponibili = []
    date_non_disponibili = db.check_date()
    return jsonify(date_non_disponibili)

@app.errorhandler(500)
def internal_server_error(e):
    #set the 500 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    helper.send_bug_report_msg(session, type(e), str(e), traceback.format_exc())
    print(traceback.format_exc())
    return render_template('error.html')

if __name__ == '__main__':
    try:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.secret_key = '6724237ce80fbd35848335402ad3a074f8b3e37a' #sha1 of my day
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()