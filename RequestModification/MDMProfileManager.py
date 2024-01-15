from XMLParserHelpers import XMLHelpers

class MDMProfileManager:
    def get_version(xml: str) -> str:
        return XMLHelpers.get_value_pair(xml, "PayloadDisplayName", "string", "key")
    
    def append_allowed_apps(xml: str, allowed_apps: list) -> str:
        current_allowed_apps = XMLHelpers.get_value_pair(xml, "allowListedAppBundleIDs", "array", "key")
        
        for app_bundle_id in allowed_apps:
            current_allowed_apps += "\n" + f"<string>{app_bundle_id}</string>" + "\n"

        xml = XMLHelpers.update_value_pair(xml, "allowListedAppBundleIDs", current_allowed_apps, "array", "key")

        return xml
    

    def update_restrictions(xml: str, restriction_modifications: dict) -> str:
        for key in restriction_modifications:
            # im probably braindead, dont care if theres other way
            boolean_value = False
            if restriction_modifications[key].lower() == "true":
                boolean_value = True

            xml = XMLHelpers.update_boolean_property(xml, key, boolean_value)

        return xml