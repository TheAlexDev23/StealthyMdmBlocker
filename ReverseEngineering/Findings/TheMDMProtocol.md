# The mdm protocol

The central dogma in mdm, is a series of tls http request-responses between the client and the mdm server.

Everything begins when a push notification is sent by the server through APNS to the device. The device then will make a PUT request to the check in url configured in the local mdm profile. The server will then respond with a command for the client to execute, upon completion of said command, the client will send another PUT request to the server mentioning the command completion (and depending on the command can also provide additional data).

What's funny is that when the client sends a request, it's usually "a response", with the status code of the last completed command. And the server resonses are rather "requests" with the next commands.

There are multiple types of commands according to the apple mdm protocol reference documentation, but this mdm solutions afaik only uses 2: ListProfiles, InstallProfile. The last one being rather an update and not a new install, as according to apple, as long as the same identity keys, url and access permissions remain the profile may be updated with InstallProfile.

See: https://developer.apple.com/business/documentation/MDM-Protocol-Reference.pdf

# Sniffed communication

Sniffing wasn't an issue. A Man-In-The-Middle proxy with custom ca certificates is enough to decrypt all requests and responses.

## PUT Request 1

Request to https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Status</key>
	<string>Idle</string>
	<key>UDID</key>
	<string>00008112-000E19103607401E</string>
</dict>
</plist>
```

## PUT Response 1
Response from https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>CommandUUID</key>
    <string>b113a1e32e5247a78d30d132a8e11c59</string>
    <key>Command</key>
    <dict>
      <key>RequestType</key>
      <string>ProfileList</string>
    </dict>
  </dict>
</plist>
```

## PUT Request 2
Request to https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CommandUUID</key>
	<string>b113a1e32e5247a78d30d132a8e11c59</string>
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
                    Base 64 encoded certificate data. When decoded, is not human readable, as it contains partially machine readable data
				</data>
				<data>
                    Base 64 encoded certificate data. When decoded, is non human readable, as it contains partially machine readable data
				</data>
				<data>
                    Base 64 encoded certificate data. When decoded, is non human readable, as it contains partially machine readable data
				</data>
			</array>
		</dict>
		<dict>
			<key>HasRemovalPasscode</key>
			<false/>
			<key>IsEncrypted</key>
			<false/>
			<key>IsManaged</key>
			<false/>
			<key>PayloadContent</key>
			<array>
				<dict>
					<key>PayloadDisplayName</key>
					<string>mitmproxy</string>
					<key>PayloadIdentifier</key>
					<string>9056de87bb3c875200e6a282301ea3f9a146f37009472dbef94a1116009d81a2a</string>
					<key>PayloadType</key>
					<string>com.apple.security.pem</string>
					<key>PayloadUUID</key>
					<string>E80D3F5E-7073-45AE-ACC6-613B8EAAF2B8</string>
					<key>PayloadVersion</key>
					<integer>1</integer>
				</dict>
			</array>
			<key>PayloadDisplayName</key>
			<string>mitmproxy</string>
			<key>PayloadIdentifier</key>
			<string>9056de87bb3c875200e6a282301ea3f9a146f37009472dbef94a1116009d81a2a</string>
			<key>PayloadRemovalDisallowed</key>
			<false/>
			<key>PayloadUUID</key>
			<string>EE75B951-7BD1-4DA3-8594-8FEFDA2C13D9</string>
			<key>PayloadVersion</key>
			<integer>1</integer>
			<key>SignerCertificates</key>
			<array>
				<data>
                    Base 64 encoded certificate data. When decoded, is non human readable, as it contains partially  machine readable data
				</data>
			</array>
		</dict>
	</array>
	<key>Status</key>
	<string>Acknowledged</string>
	<key>UDID</key>
	<string>00008112-000E19103607401E</string>
</dict>
</plist>
```

## PUT Response 2
Response from https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>CommandUUID</key>
    <string>47d6a33e3577411d9bcc4c03de2f2318</string>
    <key>Command</key>
    <dict>
      <key>RestrictionsOverrides</key>
      <array/>
      <key>CallDeviceNotifyOnAck</key>
      <false/>
      <key>RequestType</key>
      <string>InstallProfile</string>
      <key>Payload</key>
      <data>
        Base64 encrypted mdm configuration
      </data>
      <key>RestrictionOverrides</key>
      <array/>
    </dict>
  </dict>
</plist>
```

## PUT Request 3
Request to https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CommandUUID</key>
	<string>47d6a33e3577411d9bcc4c03de2f2318</string>
	<key>Status</key>
	<string>Acknowledged</string>
	<key>UDID</key>
	<string>00008112-000E19103607401E</string>
</dict>
</plist>
```

## PUT Response 3
Response from https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>CommandUUID</key>
    <string>f9908006765d429586bce3da76676184</string>
    <key>Command</key>
    <dict>
      <key>RestrictionsOverrides</key>
      <array/>
      <key>CallDeviceNotifyOnAck</key>
      <false/>
      <key>RequestType</key>
      <string>InstallProfile</string>
      <key>Payload</key>
      <key>RestrictionOverrides</key>
      <data>
        Even longer base64 encrypted mdm profile
      </data>
      <array/>
    </dict>
  </dict>
</plist>
```

## PUT Request 4

Request to https://escolainternacional.jamfcloud.com/checkin with content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CommandUUID</key>
	<string>f9908006765d429586bce3da76676184</string>
	<key>Status</key>
	<string>Acknowledged</string>
	<key>UDID</key>
	<string>00008112-000E19103607401E</string>
</dict>
</plist>
```

## PUT Response 5

Empty response

## PUT Request 6

Request to https://escolainternacional.jamfcloud.com/checkin?company=1046084&location=8116 with content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Data</key>
	<data>
        base64 encoded json
	</data>
	<key>Endpoint</key>
	<string>status</string>
	<key>MessageType</key>
	<string>DeclarativeManagement</string>
	<key>UDID</key>
	<string>00008112-000E19103607401E</string>
</dict>
</plist>
```

Decoded json

```json
{
    "StatusItems" : {
        "passcode" : {
            "is-compliant" : true
        }
    },
    "Errors" : [

    ]
}
```

## PUT Response 6

Empty json array