from flask.templating import render_template
from flask_mail import Mail, Message
import smtplib, markdown

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
