import read_settings
import helper
import mysql.connector
import hashlib
import traceback
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



def new_user(nome, cognome, data_nascita, luogo_nascita, email, cod_fis, password):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), new_user.__name__)
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

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
            helper.send_registration_email(email, nome)
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
            cursor.execute("SELECT nome, cod_fis, email FROM db_utente WHERE (email = %s AND password = %s)", 
            (email, password))
            result = cursor.fetchone()
            if cursor.rowcount == 1:
                session['loggedin'] = True
                session['nome'] = result[0]
                session['cod_fis'] = result[1]
                session['email'] = result[2]
            else:
                cursor.execute("SELECT id_amministratore FROM db_amministratori WHERE id_amministratore = %s AND password = %s", 
                (email, password))
                result = cursor.fetchone()
                if cursor.rowcount == 1:
                    session['loggedin'] = True
                    session['cod_fis'] = 'region'
                    session['nome'] = 'Amministratore'
                    session['email'] = result[0]
                else:
                    msg = '<div id="message" class="ui error mini message" style="display: none;">\
                    <div class="header">Credenziali errate</div></div>'
            cursor.close()

            # Cleanup
            conn.commit()
            conn.close()
            print("Done.")
        except Exception as e:
            msg = f'<div id="message" class="ui error mini message" style="display: none;">\
                <div class="header">Si è verificato un errore nella connessione al database</div>\
                <p>{e}</p></div>'
    return msg

def edit_vaccini(regione, num_vaccini):
    msg = 'ok'
    regione = helper.get_regione(regione)
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), edit_vaccini.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE db_regione \
                            SET num_vaccini = %s \
                            WHERE nome_regione = %s;", 
            (num_vaccini, regione))

            conn.commit()

            cursor.execute("UPDATE db_regione \
                            SET num_vaccini = (SELECT sum(num_vaccini) \
				                               FROM (SELECT * FROM db_regione) AS db_reg \
                                               WHERE nome_regione <> 'Italia') \
                            WHERE nome_regione = 'Italia';")

            cursor.close()

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), edit_vaccini.__name__)
            msg = str(e)
    return msg

def get_totale_vaccini():
    vaccini = []
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_totale_vaccini.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM db_regione")
            result = cursor.fetchall()
            vaccini = result
            cursor.close()

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_totale_vaccini.__name__)
            msg = str(e)
    if msg != 'ok':
        return msg
    return vaccini

def get_numero_vaccini(regione):
    vaccini = 0
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_numero_vaccini.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT num_vaccini FROM db_regione WHERE nome_regione = %s", (regione,))
            result = cursor.fetchone()
            if result is None:
                msg = 'not ok'
            else:
                vaccini = result[0]
            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_numero_vaccini.__name__)
            msg = str(e)
    #if msg != 'ok':
        #return msg
    return vaccini

def new_prenotazione(id_user, regione, asl, data):
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_fis, email from db_utente WHERE email = %s",(id_user,))
            result = cursor.fetchone()

            cod_fis = result[0]
            email = result[1]
            cursor.execute("INSERT INTO db_prenotazione VALUES (%s,%s,%s,%s,STR_TO_DATE(%s,'%d/%m/%Y'),false)",
            (cod_fis, email, regione, asl, data))

            cursor.execute("UPDATE db_regione SET num_vaccini = num_vaccini - 1 WHERE nome_regione = %s", (regione,))

            conn.commit()

            cursor.execute("UPDATE db_regione \
                            SET num_vaccini = (SELECT sum(num_vaccini) \
				                               FROM (SELECT * FROM db_regione) AS db_reg \
                                               WHERE nome_regione <> 'Italia') \
                            WHERE nome_regione = 'Italia';")
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
            helper.send_confirmation_email(email, asl, data)
            print("Mail sent.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), new_prenotazione.__name__)
            msg = str(e)
    return msg

def check_prenotazione(id_user):
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), check_prenotazione.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM db_prenotazione WHERE email = %s",(id_user,))
            result = cursor.fetchone()
            msg = result[0]
            
            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), check_prenotazione.__name__)
            msg = str(e)
    return msg

def get_dettagli_utente(user):
    data = {}
    #se l'utente è un amministratore il metodo non viene eseguito
    if '@' in user:
        msg = 'ok'
        try:
            conn = mysql.connector.connect(**config)
            print("Connection established")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_dettagli_utente.__name__)
            msg = str(e)
        else:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT db_utente.cod_fis, db_utente.email, nome, cognome, DATE_FORMAT(data_nascita,'%d/%m/%Y'), luogo_nascita, \
                                password, regione, asl, DATE_FORMAT(data_prenotazione,'%d/%m/%Y'), is_completed \
                                FROM db_utente LEFT JOIN db_prenotazione \
                                ON db_utente.cod_fis = db_prenotazione.cod_fis \
                                WHERE db_utente.email = %s ",(user,))
                result = cursor.fetchone()
                data['cod_fis'] = result[0]
                data['email'] = result[1]
                data['nome'] = result[2]
                data['cognome'] = result[3]
                data['data_nascita'] = result[4]
                data['luogo_nascita'] = result[5]
                data['password'] = result[6]
                data['regione'] = result[7]
                data['asl_riferimento'] = result[8]
                data['data_prenotazione'] = result[9]
                data['is_completed'] = result[10]
                cursor.close()

                # Cleanup
                cursor.close()
                conn.close()
                print("Done.")
            except Exception as e:
                helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_dettagli_utente.__name__)
                msg = str(e)
        if msg != 'ok':
            return msg
    return data

def get_prenotazioni_data(admin, data_prenotazione):
    data = {}
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_prenotazioni_data.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, cognome, cod_fis\
                            FROM db_prenotazione NATURAL JOIN db_utente \
                            WHERE asl = (SELECT asl FROM db_prenotazione NATURAL JOIN\
                                        db_amministratori \
                            WHERE id_amministratore = %s LIMIT 1) AND data_prenotazione = STR_TO_DATE(%s,'%d/%m/%Y')\
                                AND is_completed = 0"
            ,(admin, data_prenotazione))
            result = cursor.fetchall()
            if result:
                return result

            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_prenotazioni_data.__name__)
            msg = str(e)
    if msg != 'ok':
        return msg
    return data

def delete_account(email):
    msg = True
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), delete_account.__name__)
        msg = False
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM db_utente WHERE email=%s",(email,))
            
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), delete_account.__name__)
            msg = False
    return msg

def get_prenotazioni():
    prenotazioni = {}
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_prenotazioni.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM db_prenotazione WHERE is_completed = false")
            result = cursor.fetchone()
            prenotazioni['in_attesa'] = result[0]
            
            cursor.execute("SELECT COUNT(*) FROM db_prenotazione WHERE is_completed = true")
            result = cursor.fetchone()
            prenotazioni['completate'] = result[0]


            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_prenotazioni.__name__)
            msg = str(e)
    if msg != 'ok':
        return msg
    return prenotazioni

def check_date():
    date = []
    msg = 'ok'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), check_date.__name__)
        msg = str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DATE_FORMAT(data_prenotazione,'%d/%m/%Y') FROM db_prenotazione GROUP BY data_prenotazione HAVING COUNT(*) >= 6")
            result = cursor.fetchall()
            for row in result:
                date.append(row[0])
            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), check_date.__name__)
            msg = str(e)
    if msg != 'ok':
        return msg
    return date

def reset_password(email):
    msg = '<div class="ui success message">\
        <div class="header">La tua password è stata ripristinata</div>\
        <p>Controlla la tua casella di posta per maggiori informazioni.</p>\
        </div>'
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), reset_password.__name__)
        msg = f'<div class="ui error message">\
        <div class="header">Si è verificato un errore di connessione</div>\
        <p class="ui mini text">{str(e)}</p>\
        </div>'
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from db_utente WHERE email = %s",(email,))
            result = cursor.fetchall()
            if result:
                new_password = helper.get_new_password()
                cursor.execute("UPDATE db_utente SET password = %s WHERE email = %s",(hashlib.sha1(new_password.encode()).hexdigest(),email))
                helper.send_reset_password_email(email, new_password)
            else:
                msg = msg = f'<div class="ui error message">\
                <div class="header">Non esiste un utente con la mail che hai inserito</div>\
                </div>'
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), reset_password.__name__)
            msg = f'<div class="ui error message">\
            <div class="header">Si è verificato un errore di connessione</div>\
            <p>{str(e)}</p>\
            </div>'
    return msg

def change_password(old_password, new_password, email):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), change_password.__name__)
        return False
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM db_utente WHERE email = %s AND password = %s",(email, old_password))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE db_utente SET password = %s WHERE email = %s AND password = %s",(new_password, email, old_password)) 
            else:
                return False
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), change_password.__name__)
            return False
    return True

def cancel_reservation(email):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), cancel_reservation.__name__)
        return False
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM db_prenotazione WHERE email = %s ", (email,)) 

            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), cancel_reservation.__name__)
            return False
    return True

def complete_reservation(cod_fis):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), complete_reservation.__name__)
        return False
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE db_prenotazione SET is_completed = 1 WHERE \
            cod_fis = %s ",(cod_fis,)) 
            
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), complete_reservation.__name__)
            return False
    return True

def get_admin_regione(regione):
    data = []
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_admin_regione.__name__)
        return False
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM db_amministratori RIGHT JOIN db_asl ON \
                            db_amministratori.asl = db_asl.nome_asl WHERE db_asl.regione = %s",(regione,))
            result = cursor.fetchall()
            print(result)
            if result:
                for row in result:
                    data.append(row)
            else:
                return False
            # Cleanup
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), get_admin_regione.__name__)
            return False
    return data 

def insert_admin():
    asl = []
    regione = []
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except Exception as e:
        helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), insert_admin.__name__)
        return False
    else:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM db_asl")   
            result = cursor.fetchall()
            for row in result:
                asl.append(row[0])
                regione.append(row[1])
            
            for i in range(0,len(asl)):
                id_admin = f"amm_{i}_{asl[i]}".replace(" ","").replace("'","").lower()
                cursor.execute("INSERT INTO db_amministratori VALUES (%s,%s,%s,'','','24197a6cf214da8357b7bf152310be5a71f31df9')",
                (id_admin,regione[i],asl[i])) 
                print(f'Inserted: {id_admin} | {regione[i]} | {asl[i]} |  |  | 24197a6cf214da8357b7bf152310be5a71f31df9')
            # Cleanup
            conn.commit()
            cursor.close()
            conn.close()
            print("Done.")
        except Exception as e:
            helper.send_bug_report_msg(None, type(e), str(e), traceback.format_exc(), insert_admin.__name__)
            return False
    return True

if __name__ == '__main__':
    pass