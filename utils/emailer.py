# utils/emailer.py
from flask_mail import Message
from extension import mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

def send_email(subject, body, to_email, pdf_file):
    # SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    username = 'try.nachiket@gmail.com'
    password = 'ngmm cumk vjnv vopl'

    # Set up the server connection
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(username, password)

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    attachment = open(pdf_file, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf_file)}')
    msg.attach(part)

    # Send the email
    try:
        server.sendmail(username, to_email, msg.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        print("ehuiefh")
        server.quit()

