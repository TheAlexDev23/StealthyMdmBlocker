from enum import Enum

import XMLHelpers

class CommandType(Enum):
    ListProfile = 1,
    InstallProfile = 2,
    Other = 3


def get_command_type(xml: str) -> CommandType:
    string_type = XMLHelpers.get_value_pair(xml, "RequestType", "string", "key")

    if string_type == "ListProfile":
        return CommandType.ListProfile
    elif string_type == "InstallProfile":
        return CommandType.InstallProfile
    else:
        return CommandType.Other