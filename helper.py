from flask.templating import render_template
from flask_mail import Mail, Message
import smtplib

def deprecated_send_registration_email(mail, recipient, name):
    try:
        msg = Message( 
                    subject = 'Registrazione effettuata', 
                    sender = 'info.vaccitaly@gmail.com', 
                    recipients = [recipient] 
                ) 
        msg.body = f'Ciao, {name}.\n\nBenvenuto su VaccItaly.'
        mail.send(msg) 
    except Exception as e:
        print(f"exception is {e}")
        return False
    return True

def send_registration_email(recipient, name):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    s.starttls() 
    
    s.login("info.vaccitaly@gmail.com", "VaccItaly2021") 
    
    message = f"Ciao {name}, benvenuto su VaccItaly."
    
    s.sendmail("VaccItaly Support", recipient, message) 
    
    s.quit() 