import os
import smtplib
import imghdr
from email.message import EmailMessage

email = os.getenv('EMAIL')
password = os.getenv('EMAIL_PASSWORD')


msg = EmailMessage()
msg['Subject'] = "Checkout img"
msg['From'] = email
msg['To'] = email
msg.set_content("image attached")

files = ['/home/sharmaji/Khabar-board/flask_final/static/images/icon.jpg',
         '/home/sharmaji/Khabar-board/flask_final/static/images/lake.jpg',
        ]

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype=file_type,
                   filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, password)
    smtp.send_message(msg)
