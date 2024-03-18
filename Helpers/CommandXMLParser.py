from enum import Enum

import XMLHelpers


class CommandType(Enum):
    ListProfile = 1
    InstallProfile = 2
    SecurityInfo = 3
    Other = 0


def get_command_type(xml: str) -> CommandType:
    string_type = XMLHelpers.get_value_pair(xml, "RequestType", "string", "key")

    if string_type == "ProfileList":
        return CommandType.ListProfile
    elif string_type == "InstallProfile":
        return CommandType.InstallProfile
    elif string_type == "SecurityInfo":
        return CommandType.SecurityInfo
    else:
        return CommandType.Other
