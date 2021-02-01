import read_settings
import helper
import mysql.connector
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

def new_user(cod_fis, email, nome, cognome, data_nascita, luogo_nascita, password):
    try:
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

def log_user(email, password, session):
    msg = '<div id="message" class="ui success mini message" style="display: none;">\
           <div class="header">Login effettuato con successo</div></div>'
    try:
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