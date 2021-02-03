import random
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
        
def get_numero_vaccini(regione):
    return "{:,}".format(random.randint(10000, 90000))

