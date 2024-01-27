import base64

from mitmproxy import http

import CommandXMLParser
import XMLHelpers
import MDMProfileManager

from Logger import Logger
import Config

logger = Logger()


def patch_mdm_configuration(request_xml: str) -> str:
    # The mdm config is encoded for base 64. I guess for transportability reasons.
    encoded_conf = XMLHelpers.get_value_pair(request_xml, "Payload", "data", "key")
    mdm_xml = base64.b64decode(encoded_conf.encode("utf-8")).decode("utf-8")

    # The server for some fucking reason sends 2 different mdm configurations.
    # One of them seems to be for younger classes or straight up outdated.
    # This is a hardcoded check since the mdm provider has no fucking versioning rules and the one that seems to be the active has 23 in its display name.
    # However it doesn't really matter as i dont really know which profile is used so patching both should not cause any damage.
    if (
        Config.instance.PATCHING_MATCH_LATEST_VER
        and not MDMProfileManager.version_is_latest(mdm_xml)
    ):
        logger.log(
            "Will not apply patch. Not most recent version.",
            f"Decrypted mdm config:\n{mdm_xml}\nWhole response:\n{request_xml}",
        )

        return request_xml

    # Why the fuck a string isn't a reference type?

    if Config.instance.PATCHING_REMOVE_ALLOWED_APPS:
        mdm_xml = MDMProfileManager.remove_allowed_apps(mdm_xml)
    else:
        mdm_xml = MDMProfileManager.append_allowed_apps(
            mdm_xml, Config.instance.allowed_app_bundle_ids
        )

    if Config.instance.PATCHING_EXPERIMENTAL_REMOVE_APPRESTRICTIONS:
        mdm_xml = MDMProfileManager.remove_restrictions(mdm_xml)
    else:
        mdm_xml = MDMProfileManager.update_restrictions(
            mdm_xml, Config.instance.restriction_modifications
        )

    mdm_xml = MDMProfileManager.update_web_filters(mdm_xml)

    encoded_conf = base64.b64encode(mdm_xml.encode("utf-8")).decode("utf-8")

    request_xml = XMLHelpers.update_value_pair(
        request_xml, "Payload", encoded_conf, "data", "key"
    )

    logger.log(
        "Mdm Patch Applied", f"MDM config:\n{mdm_xml}\nWhole response:\n{request_xml}"
    )

    return request_xml


# mitmproxy entry
def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" not in flow.request.pretty_url:
        return

    # Should not happen, but to please pyright
    if flow.response is None:
        return

    response_text = flow.response.get_text()

    if response_text is None:
        return

    request_xml = XMLHelpers.sanitize(response_text)

    command_type = CommandXMLParser.get_command_type(request_xml)

    # no switch statements because python is top-tier brain rot.
    if command_type == CommandXMLParser.CommandType.InstallProfile:
        request_xml = patch_mdm_configuration(request_xml)
    else:
        logger.log(
            "Skipping command, unsuported type. ", f"Request xml:\n{request_xml}"
        )

    flow.response.text = request_xml


# mitmproxy entry
def request(flow: http.HTTPFlow) -> None:
    if "jamfcloud" not in flow.request.pretty_url:
        return

    request_text = flow.request.get_text()

    if request_text is None:
        return

    request_xml = XMLHelpers.sanitize(request_text)

    logger.log("Request", f"{request_xml}")
