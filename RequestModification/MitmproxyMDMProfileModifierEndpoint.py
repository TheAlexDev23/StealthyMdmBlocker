from mitmproxy import http

import base64
from os import environ

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
    # This one is not found in the restrictions category but due to the way the parser works, itll be fine
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

target_most_recent_version = False

def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" not in flow.request.pretty_url:
        return

    use_email_logging = False
    
    if environ.get("MDM_MITMPROXY_MODIFIER_USE_EMAIL") == 1:
        use_email_logging = True 
    
    request_xml = XMLHelpers.sanitize(flow.response.get_text())
    
    if CommandXMLParser.get_commandtype(request_xml) != CommandType.InstallProfile:
        if use_email_logging:        
            EmailSender.send_email(
                "Response but not install profile", 
                f"Sanitized content: {request_xml}")
        else:
            print(f"Got server non installation response.\n{request_xml}")

        return

    # The mdm config is encoded for base 64. I guess for transportability reasons
    encoded_conf = XMLHelpers.get_value_pair(request_xml, "Payload", "data", "key")
    mdm_xml = base64.b64decode(encoded_conf.encode("utf-8")).decode("utf-8")

    # The server for some fucking reason sends 2 different mdm configurations
    # One of them seems to be for younger classes or straight up outdated. 
    # This is a hardcoded check since the mdm provider has no fucking versioning rules and the one that seems to be the active has 23 in its display name
    if target_most_recent_version and "23" not in MDMProfileManager.get_version(mdm_xml):
        if use_email_logging:
            EmailSender.send_email(
                "Response install but not correct version", 
                f"Decrypted mdm config:\n{mdm_xml}\n\n\n\nSanitized content:\n{request_xml}")
        else:
            print(f"Got server installation command. But incorrect version. Mdm conf:\n{mdm_xml}")

        return
    
    # Fuck python honestly. Why isn't a string a reference type? 
    mdm_xml = MDMProfileManager.append_allowed_apps(mdm_xml, allowed_app_bundle_ids)
    mdm_xml = MDMProfileManager.update_restrictions(mdm_xml, restriction_modifications)
    mdm_xml = MDMProfileManager.update_web_filter(mdm_xml)

    encoded_conf = base64.b64encode(mdm_xml.encode("utf-8")).decode("utf-8")

    request_xml = XMLHelpers.update_value_pair(request_xml, "Payload", encoded_conf, "data", "key")

    # Can't modidy response.cotent directly since it needs to be encoded into bytes
    # and im not in the mood to search for what encoding type i need to use
    flow.response.text = request_xml

    if use_email_logging:
        EmailSender.send_email("Patch applied", f"MDM config\n: {mdm_xml}, whole response:\n {flow.response.text}")
    else:
        print(f"Patch finish. Updated conf:\n{mdm_xml}")
