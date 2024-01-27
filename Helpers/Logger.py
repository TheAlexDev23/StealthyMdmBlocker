import Config
from EmailSender import EmailSender


class Logger:
    def __init__(self):
        self._verbose = Config.instance.LOGGING_VERBOSE
        self._use_email = Config.instance.LOGGING_USE_EMAIL

        if self._use_email:
            sender_email = Config.instance.LOGGING_EMAIL
            sender_password = Config.instance.LOGGING_EMAIL_PASSWORD
            recipient = Config.instance.LOGGING_EMAIL_TARGET

            if sender_email is None or sender_password is None or recipient is None:
                raise ValueError(
                    "Incorrect configuration. "
                    + "Configured email logging without email information."
                )

            self._email_sender = EmailSender(sender_email, sender_password, recipient)

    def log(self, title: str, body: str):
        if not Config.instance.LOGGING_VERBOSE:
            body = ""

        if Config.instance.LOGGING_USE_EMAIL:
            self._email_sender.send_email(title, body)
        else:
            print(f"{title}\n{body}")
