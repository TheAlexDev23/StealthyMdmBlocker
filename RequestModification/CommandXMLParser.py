from enum import Enum

from XMLParserHelpers import XMLHelpers

class CommandType(Enum):
    ListProfile = 1,
    InstallProfile = 2,
    Other = 3


class CommandXMLParser:
    def get_commandtype(xml: str) -> CommandType:
        stringType = XMLHelpers.get_value_pair(xml, "RequestType", "string", "key")

        if stringType == "ListProfile":
            return CommandType.ListProfile
        elif stringType == "InstallProfile":
            return CommandType.InstallProfile
        else:
            return CommandType.Other