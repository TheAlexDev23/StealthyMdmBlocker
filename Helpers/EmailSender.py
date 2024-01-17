import smtplib

from email.mime.text import MIMEText
from os import environ

class EmailSender:
    def __init__(self):
        self._sender_email = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND")
        self._sender_password = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND_PSWD")
        self._recipient = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_RECEIVE")

    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self._sender_email
        msg['To'] = self._recipient

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self._sender_email, self._sender_password)
                smtp_server.sendmail(self._sender_email, self._recipient, msg.as_string())
                print("Sent mesage")
        except:
            print(f"Could not send message Sub: {subject} Body: \n {body}")
