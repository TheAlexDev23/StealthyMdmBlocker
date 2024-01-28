from os import environ
from os.path import exists

import json


class Config:
    allowed_app_bundle_ids = [
        # Native apps
        "com.apple.AppStore",
        "com.apple.weather",
        "com.apple.VoiceMemos",
        "com.apple.shortcuts",
        # Social medias
        "com.burbn.instagram",
        "com.atebits.Tweetie2",
        "com.reddit.Reddit",
        # Communication
        "com.hammerandchisel.discord",
        "ph.telegra.Telegraph",
        # Entretainment
        "com.google.ios.youtube",
        "tv.twitch",
        "com.spotify.client",
        # Videogames
        "com.valvesoftware.Steam",
        "com.activision.callofduty.shooter",
        "com.supercell.laser",
        "io.blueflower.theotown.aios",
        "com.bearbit.srw2",
        # Tools
        "com.8bit.bitwarden",
        "md.obsidian",
        "com.microblink.PhotoMath",
        "com.fogcreek.trello",
        # Proton
        "ch.protonmail.vpn",
        "ch.protonmail.protonmail",
        "ch.protonmail.drive",
        # Programming / Computer Science
        "com.crystalnix.ServerAuditor",  # This is Termius, an ssh client
        "com.github.stormbreaker.prod",
    ]

    restriction_modifications = {
        # This one is not found in the restrictions category
        # but due to the way the parser works it'll be fine.
        "PayloadRemovalDisallowed": "false",
        # restrictions category
        # fuck whoever enabled this
        "allowRemoteScreenObservation": "false",
        "allowAppInstallation": "true",
        "allowAppRemoval": "true",
        "allowInAppPurchases": "true",
        "allowAssistant": "true",
        "allowAirDrop": "true",
        "allowItunes": "true",
        "allowSafari": "true",
        "allowChat": "true",
        "allowGameCenter": "true",
        "allowMusicService": "true",
        "allowNews": "true",
        "allowSystemAppRemoval": "true",
        "allowManagedToWriteUnmanagedContacts": "true",
        "allowUnmanagedToReadManagedContacts": "true",
        "forceLimitAdTracking": "true",
        "allowPairedWatch": "true",
        "forceWifiPowerOn": "false",
        "allowVPNCreation": "true",
        "allowEraseContentAndSettings": "true",
        "allowDeviceNameModification": "true",
        "allowUIConfigurationProfileInstallation": "true",
        "allowUIAppInstallation": "true",
        "allowExplicitContent": "true",
        "allowBookstoreErotica": "true"
    }

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
        self.PATCHING_REMOVE_ALLOWED_APPS = False
        self.PATCHING_EXPERIMENTAL_REMOVE_APPRESTRICTIONS = False

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
        self.PATCHING_REMOVE_ALLOWED_APPS = patching["remove_allowed_apps"] == "1"
        self.PATCHING_EXPERIMENTAL_REMOVE_APPRESTRICTIONS = (
            patching["experimental"]["remove_app_restrictions"] == "1"
        )

    def _load_from_environment(self):
        self.LOGGING_EMAIL = self._env_get(self.LOGGING_EMAIL, "SMB_LOGGING_EMAIL")
        self.LOGGING_EMAIL_PASSWORD = self._env_get(
            self.LOGGING_EMAIL_PASSWORD, "SMB_LOGGING_EMAIL_PASSWORD"
        )
        self.LOGGING_EMAIL_TARGET = self._env_get(
            self.LOGGING_EMAIL_TARGET, "SMB_LOGGING_EMAIL_TARGET"
        )

    def _env_get(self, value: str | None, key: str) -> str | None:
        environ_value = environ.get(key)
        if environ_value is None:
            return value

        return environ_value


instance = Config()
