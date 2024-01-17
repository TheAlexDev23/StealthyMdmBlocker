import XMLHelpers

def get_version(xml: str) -> str:
    return XMLHelpers.get_value_pair(xml, "PayloadDisplayName", "string", "key")

def append_allowed_apps(xml: str, allowed_apps: list) -> str:
    current_allowed_apps = XMLHelpers.get_value_pair(xml, "allowListedAppBundleIDs", "array", "key")
    
    for app_bundle_id in allowed_apps:
        if app_bundle_id not in current_allowed_apps:
            current_allowed_apps += "\n" + f"<string>{app_bundle_id}</string>"

    xml = XMLHelpers.update_value_pair(xml, "allowListedAppBundleIDs", current_allowed_apps, "array", "key")

    return xml


def update_restrictions(xml: str, restriction_modifications: dict) -> str:
    for key in restriction_modifications:
        # there's probably another way, but it wouldn't be an issue if python used true false instead of True False
        boolean_value = False
        if restriction_modifications[key].lower() == "true":
            boolean_value = True

        xml = XMLHelpers.update_boolean_property(xml, key, boolean_value)

    return xml

def update_web_filters(xml: str) -> str:
    xml = XMLHelpers.update_boolean_property(xml, "AutoFilterEnabled", False)
    
    # Idk if making the array empty will break shit, so i give it at least 2 elements just in case
    # Nobody should suffer from these restrictions, because nobody uses bing and omegle is shut down
    updated_list = "<string>https://www.bing.com</string>\n<string>https://www.omegle.com</string>"
    xml = XMLHelpers.update_value_pair(xml, "DenyListURLs", updated_list, "array", "key")
    
    return xml