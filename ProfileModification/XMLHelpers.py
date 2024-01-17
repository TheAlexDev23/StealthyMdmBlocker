import re


def sanitize(xml: str) -> str:
    cleaned_text = re.sub(r"\\[nt\"\'\\]", "", xml)
    return cleaned_text


def get_value_pair(xml: str, key_name: str, value_tag="value", key_tag="key") -> str:
    pattern = f"<{key_tag}>{key_name}</{key_tag}>.*?<{value_tag}>(.*?)</{value_tag}>"

    matches = re.search(pattern, xml, re.DOTALL)

    if matches is None:
        return ""

    return matches.group(1)


def get_boolen_property(xml: str, key_name: str) -> bool:
    pattern = f"<key>{key_name}</key>.*?<(true|false)/>"

    matches = re.search(pattern, xml, re.DOTALL)

    if matches is None:
        return False

    if "true" in matches.group(1).lower():
        return True
    else:
        return False


def update_value_pair(
    xml: str, key_name: str, new_value: str, value_tag="value", key_tag="key"
) -> str:
    pattern = f"<{key_tag}>{key_name}</{key_tag}>.*?<{value_tag}>(.*?)</{value_tag}>"

    new_xml = re.sub(
        pattern,
        f"<{key_tag}>{key_name}</{key_tag}> <{value_tag}>{new_value}</{value_tag}>",
        xml,
        flags=re.DOTALL,
    )

    return new_xml


def update_boolean_property(xml: str, key_name: str, new_value: bool) -> str:
    pattern = f"<key>{key_name}</key>.*?<(true|false)/>"

    # Fuck python once again. Why the fuck do bools start with upper case
    new_xml = re.sub(
        pattern,
        f"<key>{key_name}</key><{str(new_value).lower()}/>",
        xml,
        flags=re.DOTALL,
    )

    return new_xml

