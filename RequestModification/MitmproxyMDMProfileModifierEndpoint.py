from mitmproxy import http

import base64

from CommandXMLParser import CommandXMLParser, CommandType
from XMLParserHelpers import XMLHelpers
from MDMProfileManager import MDMProfileManager

from EmailSender import EmailSender

# retarded, I know, but I'm not sure there's a way to use a blacklist instead of whitelist, so I'm not risking a brick on my device
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

def response(flow: http.HTTPFlow) -> None:
    if not "jamfcloud" in flow.request.pretty_url:
        return
    
    request_xml = XMLHelpers.sanitize(str(flow.response.content))
    
    if CommandXMLParser.get_commandtype(request_xml) != CommandType.InstallProfile:
        EmailSender.send_email("Response but not install profile", f"Unsanitized: {flow.response.content} \n\n\n\n Sanitized: {request_xml}")
        return

    # The mdm config is encoded for base 64. I guess for transportability reasons
    encoded_conf = XMLHelpers.get_value_pair(request_xml, "Payload", "data", "key")
    mdm_xml = base64.b64decode(encoded_conf.encode("utf-8")).decode("utf-8")

    # The server for some fucking reason sends 2 different mdm configurations
    # One of them seems to be for younger classes or straight up outdated. 
    # This is a hardcoded check since the mdm provider has no fucking versioning rules and the one that seems to be the active has 23 in its display name
    if not "23" in MDMProfileManager.get_version(mdm_xml):
        EmailSender.send_email("Response install but not correct version", f"Unsanitized: {flow.response.content} \n\n\n\n Sanitized: {request_xml} \n\n\n\n Decrypted: {mdm_xml}")
        return
    
    # Fuck python honestly. Why isn't a string a reference type? 
    mdm_xml = MDMProfileManager.append_allowed_apps(mdm_xml, allowed_app_bundle_ids)
    mdm_xml = MDMProfileManager.update_restrictions(mdm_xml, restriction_modifications)

    encoded_conf = base64.b64encode(mdm_xml.encode("utf-8")).decode("utf-8")

    request_xml = XMLHelpers.update_value_pair(request_xml, "Payload", encoded_conf, "data", "key")

    flow.response.content = request_xml

    EmailSender.send_email("Techinically all updated", f"MDM config: {request_xml}, whole response: {flow.response.content}")
