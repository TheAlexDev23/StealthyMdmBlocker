import base64
import sys

from mitmproxy import http

import CommandXMLParser
import XMLHelpers
import MDMProfileManager

from EmailSender import EmailSender

# retarded, I know, but I'm not sure there's a way to use a blacklist instead of whitelist, so I'm not risking a brick on my device.
allowed_app_bundle_ids = [
    "com.google.ios.youtube",
    "com.supercell.laser",
    "com.microblink.PhotoMath",
    "com.activision.callofduty.shooter",
    "ch.protonmail.vpn",
    "com.burbn.instagram",
    "com.atebits.Tweetie2",
    "ch.protonmail.protonmail",
    "ch.protonmail.drive"
]

restriction_modifications = {
    # This one is not found in the restrictions category but due to the way the parser works it'll be fine.
    "PayloadRemovalDisallowed"     : "false",
    
    # restrictions category 
    "allowAppInstallation"         : "true",
    "allowAppRemoval"              : "true",
    "allowInAppPurchases"          : "true",
    "allowAssistant"               : "true",
    "allowAirDrop"                 : "true",
    "allowItunes"                  : "true",
    "allowSafari"                  : "true",
    "forceWifiPowerOn"             : "false",
    "allowVPNCreation"             : "true",
    "allowEraseContentAndSettings" : "true",
    "allowDeviceNameModification"  : "true",
    "allowUIAppInstallation"       : "true"
}

# Logging configuration
use_email_logging = False
verbose: bool = "-v" in sys.argv

email_sender = EmailSender()

def log(title: str, body: str) -> None:    
    if use_email_logging:
        if verbose:
            email_sender.send_email(title, body)
        else:
            email_sender.send_email(title, "")
    else:
        if verbose:
            print(f"{title}\n{body}")
        else:
            print(f"{title}")


def patch_mdm_configuration(request_xml: str) -> str:
    target_most_recent_version = False

    # The mdm config is encoded for base 64. I guess for transportability reasons.
    encoded_conf = XMLHelpers.get_value_pair(request_xml, "Payload", "data", "key")
    mdm_xml = base64.b64decode(encoded_conf.encode("utf-8")).decode("utf-8")

    # The server for some fucking reason sends 2 different mdm configurations.
    # One of them seems to be for younger classes or straight up outdated. 
    # This is a hardcoded check since the mdm provider has no fucking versioning rules and the one that seems to be the active has 23 in its display name.
    # However it doesn't really matter as i dont really know which profile is used so patching both should not cause any damage.
    if target_most_recent_version and "23" not in MDMProfileManager.get_version(mdm_xml):
        log("Will not apply patch. Not most recent version.", f"Decrypted mdm config:\n{mdm_xml}\n\Whole response:\n{request_xml}")
        return
    
    # Fuck python honestly. Why isn't a string a reference type? 
    mdm_xml = MDMProfileManager.append_allowed_apps(mdm_xml, allowed_app_bundle_ids)
    mdm_xml = MDMProfileManager.update_restrictions(mdm_xml, restriction_modifications)
    mdm_xml = MDMProfileManager.update_web_filters(mdm_xml)

    encoded_conf = base64.b64encode(mdm_xml.encode("utf-8")).decode("utf-8")

    request_xml = XMLHelpers.update_value_pair(request_xml, "Payload", encoded_conf, "data", "key")

    log("Mdm Patch Applied", f"MDM config:\n{mdm_xml}\nWhole response:\n{request_xml}")

    return request_xml


# mitmproxy entry
def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" not in flow.request.pretty_url: 
        return

    request_xml = XMLHelpers.sanitize(flow.response.get_text())

    command_type = CommandXMLParser.get_command_type(request_xml)

    # no switch statements because python is top-tier brain rot.
    if command_type == CommandXMLParser.CommandType.InstallProfile:
        request_xml = patch_mdm_configuration(request_xml)
    else:
        log("Skipping command, unsuported type. ", f"Request xml:\n{request_xml}")
  
    flow.response.text = request_xml


# mitmproxy entry
def request(flow: http.HTTPFlow) -> None:
    if "jamfcloud" not in flow.request.pretty_url:
        return

    request_xml = XMLHelpers.sanitize(flow.response.get_text())

    log("Request", f"{request_xml}")
