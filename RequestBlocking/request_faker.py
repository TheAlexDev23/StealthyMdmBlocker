import requests

from Logger import Logger
import CommandXMLParser
from CommandXMLParser import CommandType
import XMLHelpers

TARGET = "https://escolainternacional.jamfcloud.com/checkin"
TARGET_DECLARATIVE = "https://escolainternacional.jamfcloud.com/checkin?company=1046084&location=8116"

UDID = "00008112-000E19103607401E"
HEADERS = {
    'Content-Type': 'application/x-apple-aspen-mdm; charset=UTF-8'
}

logger = Logger()

REQUEST_KILLSWITCH = 20
total_requests = 0

def send_initial_request() -> str:
    return send_request(initial_request(), TARGET, "Initial Request")


def handle_response(response: str) -> None | str:
    if response == "[]":
        return "KILL"

    if response == "":
        return send_declarative_management()

    command = CommandXMLParser.get_command_type(response)
    command_uuid = XMLHelpers.get_value_pair(response, "CommandUUID", "string", "key")

    if command is CommandType.ListProfile:
        return send_list_profiles(command_uuid)
    elif command is CommandType.InstallProfile:
        return send_profile_installed(command_uuid)
    else:
        logger.log("Command unsuported", "Attemtping to send default aknowledged")
        return send_default_aknowdleged(command_uuid)

def send_list_profiles(command_uuid: str) -> str:
    return send_request(list_profiles(command_uuid), TARGET, "List Profiles")


def send_profile_installed(command_uuid: str) -> str:
    return send_request(profile_installed(command_uuid), TARGET, "Profile Installed")


def send_default_aknowdleged(command_uuid: str) -> str:
    return send_request(default_aknowledged(command_uuid), TARGET, "Default Acknowdleged")


def send_declarative_management() -> str:
    return send_request(declarative_management(), TARGET_DECLARATIVE, "Declarative Management")


def send_request(body, target, name):
    global total_requests

    if total_requests >= REQUEST_KILLSWITCH:
        print("KILLSWITCH")
        return "KILL"

    logger.log(f"{name} request", body);
    response = requests.put(target, headers=HEADERS, data=body)
    total_requests += 1
    logger.log(f"{name} response {response.status_code}", response.text)

    if response.status_code != 200:
        return "KILL"
    else:
        return response.text


def initial_request() -> str:
    return f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Status</key>
        <string>Idle</string>
        <key>UDID</key>
        <string>{UDID}</string>
    </dict>
    </plist>
    """

def list_profiles(command_uuid: str) -> str:
    return f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CommandUUID</key>
        <string>{command_uuid}</string>
        <key>ProfileList</key>
        <array>
            <dict>
                <key>HasRemovalPasscode</key>
                <false/>
                <key>IsEncrypted</key>
                <false/>
                <key>IsManaged</key>
                <true/>
                <key>PayloadContent</key>
                <array>
                    <dict>
                        <key>PayloadDisplayName</key>
                        <string>1046084.mdm.zuludesk.com</string>
                        <key>PayloadIdentifier</key>
                        <string>58f9938f-aa4f-4637-b6d7-404d6f09ebf0</string>
                        <key>PayloadType</key>
                        <string>com.apple.security.pkcs12</string>
                        <key>PayloadUUID</key>
                        <string>58f9938f-aa4f-4637-b6d7-404d6f09ebf0</string>
                        <key>PayloadVersion</key>
                        <integer>1</integer>
                    </dict>
                    <dict>
                        <key>PayloadDisplayName</key>
                        <string>Enrollment</string>
                        <key>PayloadIdentifier</key>
                        <string>d315b8f3-13ba-443c-832c-e39ea5e8a688</string>
                        <key>PayloadType</key>
                        <string>com.apple.mdm</string>
                        <key>PayloadUUID</key>
                        <string>d315b8f3-13ba-443c-832c-e39ea5e8a688</string>
                        <key>PayloadVersion</key>
                        <integer>1</integer>
                    </dict>
                </array>
                <key>PayloadDescription</key>
                <string>Mobile Device Management Configuration</string>
                <key>PayloadDisplayName</key>
                <string>Jamf School MDM Profile (version:1)</string>
                <key>PayloadIdentifier</key>
                <string>com.apple.mdm</string>
                <key>PayloadOrganization</key>
                <string>Escola Internacional Del Camp</string>
                <key>PayloadRemovalDisallowed</key>
                <true/>
                <key>PayloadUUID</key>
                <string>aa23d0e4-6978-4afe-88a5-8fc058676001</string>
                <key>PayloadVersion</key>
                <integer>1</integer>
                <key>SignerCertificates</key>
                <array>
                    <data>
                    MIIGNjCCBR6gAwIBAgIQTyoUAqMKfBWw9dgj0kLk5zAN
                    BgkqhkiG9w0BAQsFADCBjzELMAkGA1UEBhMCR0IxGzAZ
                    BgNVBAgTEkdyZWF0ZXIgTWFuY2hlc3RlcjEQMA4GA1UE
                    BxMHU2FsZm9yZDEYMBYGA1UEChMPU2VjdGlnbyBMaW1p
                    dGVkMTcwNQYDVQQDEy5TZWN0aWdvIFJTQSBEb21haW4g
                    VmFsaWRhdGlvbiBTZWN1cmUgU2VydmVyIENBMB4XDTIz
                    MDMyMTAwMDAwMFoXDTI0MDQyMDIzNTk1OVowGjEYMBYG
                    A1UEAwwPKi5qYW1mY2xvdWQuY29tMIIBIjANBgkqhkiG
                    9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5llWu2fWalAjJt+H
                    MKGARLSMs3UhW6+J+ppTY5CJq9hibqNA3ZxrVrr0daQC
                    WlH/wKfX1N7fnHJ05LUoM72K1TUFqE1vnvx5Z1dnXmv1
                    xOcDNoIXUIcPDFlywI14dZTocfy0cRVebHLyqpoQ6wj1
                    RbAIKxz4lnU/4K+iWwUuGLpZDVfHTOWz1gXeP/k1La8T
                    f3Brcy+UF10OOk7zKRSH1mN5tien0g2cTrMR7fN695Yz
                    Y29gcgFnHi0JbM2oOfcoNaed4EneTy+WnnI9PQ/cXloE
                    oS0SogOtZIb2PhFN1YzpasPCINYY0Z1rFPXBgqcqqPqg
                    Lo3D3oo85hLK2mwRuwIDAQABo4IDADCCAvwwHwYDVR0j
                    BBgwFoAUjYxexFStiuF36Zv5mwXhuAGNYeEwHQYDVR0O
                    BBYEFKnE0zdm6d23yEkVjh/6/zCTNMuiMA4GA1UdDwEB
                    /wQEAwIFoDAMBgNVHRMBAf8EAjAAMB0GA1UdJQQWMBQG
                    CCsGAQUFBwMBBggrBgEFBQcDAjBJBgNVHSAEQjBAMDQG
                    CysGAQQBsjEBAgIHMCUwIwYIKwYBBQUHAgEWF2h0dHBz
                    Oi8vc2VjdGlnby5jb20vQ1BTMAgGBmeBDAECATCBhAYI
                    KwYBBQUHAQEEeDB2ME8GCCsGAQUFBzAChkNodHRwOi8v
                    Y3J0LnNlY3RpZ28uY29tL1NlY3RpZ29SU0FEb21haW5W
                    YWxpZGF0aW9uU2VjdXJlU2VydmVyQ0EuY3J0MCMGCCsG
                    AQUFBzABhhdodHRwOi8vb2NzcC5zZWN0aWdvLmNvbTAp
                    BgNVHREEIjAggg8qLmphbWZjbG91ZC5jb22CDWphbWZj
                    bG91ZC5jb20wggF+BgorBgEEAdZ5AgQCBIIBbgSCAWoB
                    aAB2AHb/iD8KtvuVUcJhzPWHujS0pM27KdxoQgqf5mdM
                    Wjp0AAABhwOvSwQAAAQDAEcwRQIhAPbr0uNIF1oYcRg3
                    feiqhs0h4zrmc4jLogzUJd+wmglDAiAOjcVfqP/8c6Xm
                    xxhkekMu3UV/2Asxn5F6vZiuWN+BvgB3ANq2v2s/tbYi
                    n5vCu1xr6HCRcWy7UYSFNL2kPTBI1/urAAABhwOvS2cA
                    AAQDAEgwRgIhAKyCoszjjK4sccW4D4hhsjYfBYbHdr78
                    j7/DVjdMPVDtAiEAhpd98Iz98SiN/SNiSnPnCLhU04pe
                    k2ZM0ZIKPoc0sfwAdQDuzdBk1dsazsVct520zROiModG
                    fLzs3sNRSFlGcR+1mwAAAYcDr0szAAAEAwBGMEQCICKv
                    2dd3k4v6xcawDwFyiInTNe6s8q4LLbOCQp4d3kLxAiA9
                    q6gSXgssr2W5lCzaDFGMDSU81Mu55y26bicbFnF8oTAN
                    BgkqhkiG9w0BAQsFAAOCAQEAz1+R6OFjKv+6ekVnbNxh
                    J/xBIgcy66CmRrhtjCv4NwtlwVhM4/FFyTvlchI0X9u5
                    0EkCk4OIOiAJSGfFONh6OJKofiop2Kzw5i97Q2Vh2N+t
                    k37ZS2rszY9oAQdALnLf67w9WO+ayVY88Y+j4o8tQkFe
                    qagWlYMqb5p/o5UuwDWb33jFZsfWXA0XtPNkQhS/9Ry6
                    zwxCzdM3sARoGCPUAdWpAPWopxZy/hHLYMnE0mr4CoI/
                    onRn7ZG+yQSqtDGSAXdtpk4ZfD4u/Khr/LN3Jg4mC9hA
                    6KHoddwLMed5DIAyd4tvvZskc2kI+73Af5kyXAborOk/
                    zKwKlxo+XFDhgw==
                    </data>
                    <data>
                    MIIFgTCCBGmgAwIBAgIQOXJEOvkit1HX02wQ3TE1lTAN
                    BgkqhkiG9w0BAQwFADB7MQswCQYDVQQGEwJHQjEbMBkG
                    A1UECAwSR3JlYXRlciBNYW5jaGVzdGVyMRAwDgYDVQQH
                    DAdTYWxmb3JkMRowGAYDVQQKDBFDb21vZG8gQ0EgTGlt
                    aXRlZDEhMB8GA1UEAwwYQUFBIENlcnRpZmljYXRlIFNl
                    cnZpY2VzMB4XDTE5MDMxMjAwMDAwMFoXDTI4MTIzMTIz
                    NTk1OVowgYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpO
                    ZXcgSmVyc2V5MRQwEgYDVQQHEwtKZXJzZXkgQ2l0eTEe
                    MBwGA1UEChMVVGhlIFVTRVJUUlVTVCBOZXR3b3JrMS4w
                    LAYDVQQDEyVVU0VSVHJ1c3QgUlNBIENlcnRpZmljYXRp
                    b24gQXV0aG9yaXR5MIICIjANBgkqhkiG9w0BAQEFAAOC
                    Ag8AMIICCgKCAgEAgBJlFzYOw9sIs9CsVw127c0n00yt
                    UINh4qogTQktZAnczomfzD2p7PbPwdzx07HWezcoEStH
                    2jnGvDoZtF+mvX2do2NCtnbyqTsrkfjib9DsFiCQCT7i
                    6HTJGLSR1GJk23+jBvGIGGqQIjy8/hPwhxR79uQfjtTk
                    UcYRZ0YIUcuGFFQ/vDP+fmyc/xadGL1RjjWmp2bIcmfb
                    IWax1Jt4A8BQOujM8Ny8nkz+rwWWNR9XWrf/zvk9tyy2
                    9lTdyOcSOk2uTIq3XJq0tyA9yn8iNK5+O2hmAUTnAU5G
                    U5szYPeUvlM3kHND8zLDU+/bqv50TmnHa4xgk97Exwzf
                    4TKuzJM7UXiVZ4vuPVb+DNBpDxsP8yUmazNt925H+nND
                    5X4OpWaxKXwyhGNVicQNwZNUMBkTrNN9N6frXTpsNVzb
                    QdcS2qlJC9/YgIoJk2KOtWbPJYjNhLixP6Q5D9kCnusS
                    TJV882sFqV4Wg8y4Z+LoE53MW4LTTLPtW//e5XOsIzst
                    AL81VXQJSdhJWBp/kjbmUZIO8yZ9HE0XvMnsQybQv0Ff
                    QKlERPSZ51eHnlAfV1SoPv10Yy+xUGUJ5lhCLkMaTLTw
                    JUdZ+gQek9QmRkpQgbLevni3/GcV4clXhB4PY9bpYrrW
                    X1Uu6lzGKAgEJTm4Diup8kyXHAc/DVL17e8vgg8CAwEA
                    AaOB8jCB7zAfBgNVHSMEGDAWgBSgEQojPpbxB+zirynv
                    gqV/0DCktDAdBgNVHQ4EFgQUU3m/WqorSs9UgOHYm8Cd
                    8rIDZsswDgYDVR0PAQH/BAQDAgGGMA8GA1UdEwEB/wQF
                    MAMBAf8wEQYDVR0gBAowCDAGBgRVHSAAMEMGA1UdHwQ8
                    MDowOKA2oDSGMmh0dHA6Ly9jcmwuY29tb2RvY2EuY29t
                    L0FBQUNlcnRpZmljYXRlU2VydmljZXMuY3JsMDQGCCsG
                    AQUFBwEBBCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29j
                    c3AuY29tb2RvY2EuY29tMA0GCSqGSIb3DQEBDAUAA4IB
                    AQAYh1HcdCE9nIrgJ7cz0C7M7PDmy14R3iJvm3WOnnL+
                    5Nb+qh+cli3vA0p+rvSNb3I8QzvAP+u431yqqcau8vzY
                    7qN7Q/aGNnwU4M309z/+3ri0ivCRlv79Q2R+/czSAaF9
                    ffgZGclCKxO/WIu6pKJmBHaIkU4MiRTOok3JMrO66BQa
                    vHHxW/BBC5gACiIDEOUMsfnNkjcZ7Tvx5Dq2+UUTJnWv
                    u6rvP3t3O9LEApE9GQDTF1w52z97GA1FzZOFli9d31kW
                    Tz9RvdVFGD/tSo7oBmF0Ixa1DVBzJ0RHfxBdiSprhTEU
                    xOipakyAvGp4z7h/jnZymQyd/teRCBaho1+V
                    </data>
                    <data>
                    MIIGEzCCA/ugAwIBAgIQfVtRJrR2uhHbdBYLvFMNpzAN
                    BgkqhkiG9w0BAQwFADCBiDELMAkGA1UEBhMCVVMxEzAR
                    BgNVBAgTCk5ldyBKZXJzZXkxFDASBgNVBAcTC0plcnNl
                    eSBDaXR5MR4wHAYDVQQKExVUaGUgVVNFUlRSVVNUIE5l
                    dHdvcmsxLjAsBgNVBAMTJVVTRVJUcnVzdCBSU0EgQ2Vy
                    dGlmaWNhdGlvbiBBdXRob3JpdHkwHhcNMTgxMTAyMDAw
                    MDAwWhcNMzAxMjMxMjM1OTU5WjCBjzELMAkGA1UEBhMC
                    R0IxGzAZBgNVBAgTEkdyZWF0ZXIgTWFuY2hlc3RlcjEQ
                    MA4GA1UEBxMHU2FsZm9yZDEYMBYGA1UEChMPU2VjdGln
                    byBMaW1pdGVkMTcwNQYDVQQDEy5TZWN0aWdvIFJTQSBE
                    b21haW4gVmFsaWRhdGlvbiBTZWN1cmUgU2VydmVyIENB
                    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
                    1nMz1tc8INAA0hdFuNY+B6I/x0HuMjDJsGz99J/LEpgP
                    LT+NTQEMgg8Xf2Iu6bhIefsWg06t1zIlk7cHv7lQP6lM
                    w0Aq6Tn/2YHKHxYyQdqAJrkjeocgHuP/IJo8lURvh3UG
                    kEC0MpMWCRAIIz7S3YcPb11RFGoKacVPAXJpz9OTTG0E
                    oKMbgn6xmrntxZ7FN3ifmgg0+1YuWMQJDgZkW7w33PGf
                    KGioVrCSo1yfu4iYCBskHaswha6vsC6eep3BwEIc4gLw
                    6uBK0u+QDrTBQBbwb4VCSmT3pDCg/r8uoydajotYuK3D
                    GReEY+1vVv2Dy2A0xHS+5p3b4eTlygxfFQIDAQABo4IB
                    bjCCAWowHwYDVR0jBBgwFoAUU3m/WqorSs9UgOHYm8Cd
                    8rIDZsswHQYDVR0OBBYEFI2MXsRUrYrhd+mb+ZsF4bgB
                    jWHhMA4GA1UdDwEB/wQEAwIBhjASBgNVHRMBAf8ECDAG
                    AQH/AgEAMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEF
                    BQcDAjAbBgNVHSAEFDASMAYGBFUdIAAwCAYGZ4EMAQIB
                    MFAGA1UdHwRJMEcwRaBDoEGGP2h0dHA6Ly9jcmwudXNl
                    cnRydXN0LmNvbS9VU0VSVHJ1c3RSU0FDZXJ0aWZpY2F0
                    aW9uQXV0aG9yaXR5LmNybDB2BggrBgEFBQcBAQRqMGgw
                    PwYIKwYBBQUHMAKGM2h0dHA6Ly9jcnQudXNlcnRydXN0
                    LmNvbS9VU0VSVHJ1c3RSU0FBZGRUcnVzdENBLmNydDAl
                    BggrBgEFBQcwAYYZaHR0cDovL29jc3AudXNlcnRydXN0
                    LmNvbTANBgkqhkiG9w0BAQwFAAOCAgEAMr9hvQ5Iw0/H
                    ukdN+Jx4GQHcEx2Ab/zDcLRSmjEzmldS+zGea6TvVKqJ
                    jUAXaPgREHzSyrHxVYbH7rM2kYb2OVG/Rr8PoLq0935J
                    xCo2F57kaDl6r5ROVm+yezu/Coa9zcV3HAO4OLGiH19+
                    24rcRki2aArPsrW04jTkZ6k4Zgle0rj8nSg6F0AnwnJO
                    Kf0hPHzPE/uWLMUxRP0T7dWbqWlod3zu4f+k+TY4CFM5
                    ooQ0nBnzvg6s1SQ36yOoeNDT5++SR2RiOSLvxvcRviKF
                    xmZEJCaOEDKNyJOuB56DPi/Z+fVGjmO+wea03KbNIaiG
                    CpXZLoUmGv38sbZXQm2V0TP2ORQGgkE49Y9Y3IBbpNV9
                    lXj9p5v//cWoaasm56ekBYdbqbe4oyALl6lFhd2zi+WJ
                    N44pDfwGF/Y4QA5C5BIG+3vzxhFoYt/jmPQT2BVPi7Fp
                    2RBgvGQq6jG35LWjOhSbJuMLe/0CjraZwTiXWTb2qHSi
                    hrZe68Zk6s+go/lunrotEbaGmAhYLcmsJWTyXnW0OMGu
                    f1pGg+pRyrbxmRE1a6Vqe8YAsOf4vmSyrcjC8azjUeqk
                    k+B5yOGBQMkKW+ESPMFgKuOXwIlCypTPRpgSabuY0MLT
                    DXJLR27lk8QyKGOHQ+SwMj4K00u/I5sUKUErmgQfky3x
                    xzlIPK1aEn8=
                    </data>
                </array>
            </dict>
        </array>
        <key>Status</key>
        <string>Acknowledged</string>
        <key>UDID</key>
        <string>{UDID}</string>
    </dict>
    </plist>
    """

def profile_installed(command_uuid: str) -> str:
    return default_aknowledged(command_uuid)

def default_aknowledged(command_uuid: str) -> str:
    return f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CommandUUID</key>
        <string>{command_uuid}</string>
        <key>Status</key>
        <string>Acknowledged</string>
        <key>UDID</key>
        <string>{UDID}</string>
    </dict>
    </plist>
    """

def declarative_management() -> str:
    return f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Data</key>
        <data>
            ewogICAgIlN0YXR1c0l0ZW1zIiA6IHsKICAgICAgICAicGFzc2NvZGUiIDogewogICAgICAgICAg
            ICAiaXMtY29tcGxpYW50IiA6IHRydWUKICAgICAgICB9CiAgICB9LAogICAgIkVycm9ycyIgOiBb
            CgogICAgXQp9Cg==
        </data>
        <key>Endpoint</key>
        <string>status</string>
        <key>MessageType</key>
        <string>DeclarativeManagement</string>
        <key>UDID</key>
        <string>{UDID}</string>
    </dict>
    </plist>
    """
