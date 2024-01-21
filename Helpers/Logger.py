from os import environ

import Config
from EmailSender import EmailSender


class Logger:
    def __init__(self):
        self._verbose = Config.instance.LOGGING_VERBOSE
        self._use_email = Config.instance.LOGGING_USE_EMAIL

        self._sender_email = Config.instance.LOGGING_EMAIL
        self._sender_password = Config.instance.LOGGING_EMAIL_PASSWORD
        self._recipient = Config.instance.LOGGING_EMAIL_TARGET

        if self._use_email:
            self._email_sender = EmailSender()

    def log(self, title: str, body: str):
        if not Config.instance.LOGGING_VERBOSE:
            body = ""

        if Config.instance.LOGGING_USE_EMAIL:
            self._email_sender.send_email(title, body)
        else:
            print(f"{title}\n{body}")
