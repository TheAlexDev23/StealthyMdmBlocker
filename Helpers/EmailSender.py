from os import environ

import smtplib
from email.mime.text import MIMEText

import Config


class EmailSender:
    def __init__(self):
        self._sender = Config.instance.LOGGING_EMAIL
        self._password = Config.instance.LOGGING_EMAIL_PASSWORD
        self._recipient = Config.instance.LOGGING_EMAIL_TARGET

    def send_email(self, subject, body):
        sender = self._sender
        password = self._password
        recipient = self._recipient

        if sender is None or password is None or recipient is None:
            return

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipient, msg.as_string())
                print("Sent mesage")
        except:
            print(f"Could not send message Sub: {subject} Body: \n {body}")
