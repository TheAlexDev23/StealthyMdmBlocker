import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, sender: str, password: str, recipient: str):
        self._sender = sender
        self._password = password
        self._recipient = recipient

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
