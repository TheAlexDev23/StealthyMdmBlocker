import os

restriction_modifications = {
    "PayloadRemovalDisallowed": "false",
    "allowAppInstallation": "true",
}

allowed_app_bundle_ids = ["com.apple.AppStore", "com.google.ios.youtube"]


def get_profile_modification_path() -> str:
    path = os.getcwd()
    path += "/../ProfileModification/"
    return path


def get_helpers_path() -> str:
    path = os.getcwd()
    path += "/../Helpers/"
    return path
