from os import environ
from os.path import exists

import json


class Config:
    def __init__(self):
        self._set_defaults()
        self._load_from_json()
        self._load_from_environment()

    def _set_defaults(self):
        self.LOGGING_VERBOSE = False
        self.LOGGING_USE_EMAIL = False
        self.LOGGING_EMAIL = None
        self.LOGGING_EMAIL_PASSWORD = None
        self.LOGGING_EMAIL_TARGET = None

        self.PATCHING_MATCH_LATEST_VER = False
        self.PATCHING_EXPERIMENTAL_REMOVE_ALLOWED_APPS = False

    def _load_from_json(self):
        if not exists("/etc/SMB/config.json"):
            return

        config_file = open("/etc/SMB/config.json")
        data = json.load(config_file)
        config_file.close()

        logging = data["logging"]

        self.LOGGING_VERBOSE = logging["verbose"] == "1"
        self.LOGGING_USE_EMAIL = logging["use_email"] == "1"

        patching = data["patching"]

        self.PATCHING_MATCH_LATEST_VER = patching["match_latest_version"] == "1"
        self.PATCHING_EXPERIMENTAL_REMOVE_ALLOWED_APPS = (
            patching["experimental"]["remove_allowed_apps"] == "1"
        )

    def _load_from_environment(self):
        self.LOGGING_EMAIL = self._env_get(self.LOGGING_EMAIL, "SMB_LOGGING_EMAIL")
        self.LOGGING_EMAIL_PASSWORD = self._env_get(
            self.LOGGING_EMAIL_PASSWORD, "SMB_LOGGING_EMAIL_PASSWORD"
        )
        self.LOGGING_EMAIL_TARGET = self._env_get(
            self.LOGGING_EMAIL_TARGET, "SMB_LOGGING_EMAIL_TARGET"
        )

    def _env_get(self, value: str, key: str) -> str:
        environ_value = environ.get(key)
        if environ_value is None:
            return value

        return environ_value


instance = Config()
