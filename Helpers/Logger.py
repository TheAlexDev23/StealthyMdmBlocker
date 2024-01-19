from os import environ

from EmailSender import EmailSender


class Logger:
    def __init__(self):
        self._use_email = True
        self._verbose = True

        self._sender_email = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND")
        self._sender_password = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_SEND_PSWD")
        self._recipient = environ.get("MDM_MITMPROXY_NOTIFIER_EMAIL_RECEIVE")

        if self._use_email:
            self._email_sender = EmailSender()

    def log(self, title: str, body: str):
        # temporary, remove
        print(f"{title}\n{body}")

        if not self._verbose:
            body = ""

        if self._use_email:
            self._email_sender.send_email(title, body)
        else:
            print(f"{title}\n{body}")

