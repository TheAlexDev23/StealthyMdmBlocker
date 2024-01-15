import smtplib

from email.mime.text import MIMEText
from os import environ

class EmailSender:
    def send_email(subject, body):
        sender_email = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND")
        sender_password = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND_PSWD")
        recipient = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_RECEIVE")

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender_email, sender_password)
                smtp_server.sendmail(sender_email, recipient, msg.as_string())
                print("Sent mesage")
        except:
            print(f"Could not send message Sub: {subject} Body: \n {body}")