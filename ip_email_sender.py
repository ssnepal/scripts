import socket
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address= s.getsockname()[0]
print(ip_address)
s.close()

def_email = os.getenv("EMAIL")
def_pass = os.getenv("EMAIL_PASSWORD")
msg = '{0}:8888 Jupyter server running'.format(ip_address)

def send_email(sender=def_email, email=def_email, password=def_pass,
                receiver=def_email, msg=msg):

    #Ports 465 and 587 are intended for email client to email server communication - sending email
    server = smtplib.SMTP('smtp.gmail.com', 587)

    #starttls() is a way to take an existing insecure connection and upgrade it to a secure connection using SSL/TLS.
    server.starttls()

    #Next, log in to the server
    server.login(email, password)

    master_message = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = msg
    master_message['From']=email
    master_message['To']=email
    master_message['Subject']="Jupyter_Notebook"

    master_message.attach(MIMEText(message, 'plain'))

    #Send the mail
    server.send_message(master_message)

if __name__ == '__main__':
    send_email()
