from hashlib import new
import random, string
from flask import jsonify
import time
import smtplib
import csv

def send_registration_email(recipient, name):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
  
    server.starttls() 
    
    server.login("info.vaccitaly@gmail.com", "VaccItaly2021")
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    multipart_msg = MIMEMultipart("alternative")

    multipart_msg["Subject"] = 'Registrazione effettuata'
    multipart_msg["From"] = 'VaccItaly Support' + f' <info.vaccitaly@gmail.com>'
    multipart_msg["To"] = recipient

    message = f'Ciao {name}, grazie per esserti registrato a VaccItaly.'

    text = message
    html = f'<html>\
            <body>\
            <p>Ciao {name},<br>\
            grazie per esserti registrato a VaccItaly. Se già sai come funziona il sito, puoi prenotare un appuntamento\
            <a href="#">cliccando qui</a>.</p>\
            <p>Se vuoi sapere di più su come funziona, ti consigliamo di dare un\'occhiata <a href="#">qui</a>.</p>\
            <p></p>\
            <p></p>\
            <p style="margin-top=3em;" >Il team di VaccItaly</p>\
            </body>\
            </html>'

    part1 = MIMEText(text, "plain", "utf-8")
    part2 = MIMEText(html, "html", "utf-8")

    multipart_msg.attach(part1)
    multipart_msg.attach(part2)

    server.sendmail('info.vaccitaly@gmail.com', recipient,
                                multipart_msg.as_string().encode('utf-8'))

def send_bug_report_msg(session, exception_type, exception_msg, traceback):

    recipient = 'info.vaccitaly@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587) 
  
    server.starttls() 
    
    server.login("info.vaccitaly@gmail.com", "VaccItaly2021")
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    multipart_msg = MIMEMultipart("alternative")

    multipart_msg["Subject"] = 'VaccItaly Auto Bug Report'
    multipart_msg["From"] = 'VaccItaly Support' + f' <info.vaccitaly@gmail.com>'
    multipart_msg["To"] = recipient

    message = '----------USER----------\n\n' + str(session['loggedin']) + '\n' + str(session['nome']) + \
               '\n' + str(session['cod_fis']) + '\n\n\n' + \
    '----------TYPE----------\n\n' + str(exception_type) + '\n\n\n' + \
    '----------MESSAGE----------\n\n' + exception_msg + '\n\n\n' + '----------TRACEBACK----------\n\n' + traceback

    text = message

    part1 = MIMEText(text, "plain", "utf-8")

    multipart_msg.attach(part1)

    server.sendmail('info.vaccitaly@gmail.com', recipient,
                                multipart_msg.as_string().encode('utf-8'))

def send_confirmation_email(email, asl, data):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
  
    server.starttls() 
    
    server.login("info.vaccitaly@gmail.com", "VaccItaly2021")
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    multipart_msg = MIMEMultipart("alternative")

    multipart_msg["Subject"] = 'Conferma prenotazione'
    multipart_msg["From"] = 'VaccItaly Support' + f' <info.vaccitaly@gmail.com>'
    multipart_msg["To"] = email

    message = f'Grazie per aver prenotato un appuntamento con VaccItaly.\
               \n\nIl tuo appuntamento è previsto per il giorno {data} \
               presso {asl}. Ricorda di portare con te un documento di riconoscimento.\
               \n\n\nIl team di VaccItaly'

    text = message
    html = f'<html>\
            <body>\
            <p>Grazie per aver prenotato un appuntamento con VaccItaly.</p>\
            <p>Il tuo appuntamento è previsto per il giorno {data} \
               presso {asl}. Ricorda di portare con te un documento di riconoscimento.</p>\
                </p>\
               <br>\
               <br><p style="margin-top=2em;">Il team di VaccItaly</p>\
            </body>\
            </html>'

    part1 = MIMEText(text, "plain", "utf-8")
    part2 = MIMEText(html, "html", "utf-8")

    multipart_msg.attach(part1)
    multipart_msg.attach(part2)

    server.sendmail('info.vaccitaly@gmail.com', email,
                                multipart_msg.as_string().encode('utf-8'))

def send_reset_password_email(email, new_password):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
  
    server.starttls() 
    
    server.login("info.vaccitaly@gmail.com", "VaccItaly2021")
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    multipart_msg = MIMEMultipart("alternative")

    multipart_msg["Subject"] = 'Recupero password'
    multipart_msg["From"] = 'VaccItaly Support' + f' <info.vaccitaly@gmail.com>'
    multipart_msg["To"] = email

    message = f'Ciao, di seguito la tua password provvisoria:\
               \n\n{new_password}\
               \n\nTi consigliamo di cambiare la password al tuo prossimo accesso.\
               \n\n\nIl team di VaccItaly'

    text = message
    html = f'<html>\
            <body>\
            <p>Ciao, di seguito la tua password provvisoria:</p>\
            <p>{new_password}</p>\
               <br><p style="margin-top=2em;">Ti consigliamo di cambiare la password al tuo prossimo accesso.</p>\
               <br><p style="margin-top=2em;">Il team di VaccItaly</p>\
            </body>\
            </html>'

    part1 = MIMEText(text, "plain", "utf-8")
    part2 = MIMEText(html, "html", "utf-8")

    multipart_msg.attach(part1)
    multipart_msg.attach(part2)

    server.sendmail('info.vaccitaly@gmail.com', email,
                                multipart_msg.as_string().encode('utf-8'))

def get_elenco_comuni(regione):
    f = open('asl.csv')
    csv_f = csv.reader(f)

    lista_comuni = []
    
    for row in csv_f:
            dictionary = {}
            row = row[0].split(';')
            #print(row[6])
            dictionary['category'] = row[2].strip().title()
            dictionary['name'] = row[6].title()
            dictionary['value'] = row[6].title()
            dictionary['asl'] = row[4].title()
            #print(dictionary)
            if (dictionary['category'] == regione):
                    lista_comuni.append(dictionary)
    return jsonify(lista_comuni)
        
def get_regione(regione):
    result = regione
    if (regione == 'emiliaromagna'):
        result = 'Emilia Romagna'
    elif (regione == 'friuliveneziagiulia'):
        result = 'Friuli Venezia Giulia'
    elif (regione == 'pabolzano'):
        result = 'Prov. Auton. Bolzano'
    elif (regione == 'patrento'):
        result = 'Prov. Auton. Trento'
    elif (regione == 'valledaosta'):
        result = "Valle D'Aosta"
    return result

def get_new_password():
    new_pass = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    return new_pass

