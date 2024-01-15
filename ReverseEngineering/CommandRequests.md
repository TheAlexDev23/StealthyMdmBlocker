# Command requests

# InstallProfile command

Seems to be the main and most important command, since it has all the profile configuration. And the one that seems the most exploitable.

## Highlights

Can help to know what kind of command this is

```xml
<key>RequestType</key>
<string>InstallProfile</string>
```

Actual configuration. It's base64 encrypted look at decrypted analysis [here](./DecryptedConfigurationProfiles.md)

```xml
<data>
**Long af base64 encoded mdm configuration**
</data>
```


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
      <data>
        **Long af base64 encoded mdm configuration**
      </data>
      <key>RestrictionOverrides</key>
      <array/>
    </dict>
  </dict>
</plist>
```