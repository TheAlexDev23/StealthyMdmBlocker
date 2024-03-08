# Stealthy MDM Blocker

My attempt at silently blocking mdm functionality. Reverse engineered findings of the mdm functionality can be found [here](./ReverseEngineering/Findings/).

The current solution is essentially a MITM proxy with custom CA certificates that can decrypt and modify outgoing requests and incoming responses to the mdm server. The main solution found [here](./ProfileModification/), is able to differentiate the possible messages that can happen between the client and the server, decode the mdm configuration, modify it to remove most of the restrictions and encode it back again.

The thing is fully undetectable to the MDM server, but I got snitched out because thats the only fucking way I could get caught. They gavce me a 24hour x 1month ban. This was problematic for me as the way the blocker currently works is by modifying morning requests and I assume (as I could not reverse engineer those at that time, so I could be wrong) they just extend the <key>DeletionDate</key> field [see more](./ReverseEngineering/Findings/DecryptedConfigurationProfiles.md) to a month further. In this case no requests should be sent in the morning. Anyways, I couldn't verify it as I accidentally system reset the ipad when fucking around with libimobiledevice, that's when I could install a configuration profile again with no issues. 

After some time though, I realized that requesets aren't even sent in the mornings after an os reset, and that the MDM does not work even without the mitm proxy. I still don't 100% why that happens, but I assume it's because during reset a /checkout PUT request is sent to the MDM server which then stops sending push notis and consequently no http communication. 

The thing is written in python because mitmproxy (my MITM proxy of choice) only has request/response editing modules for python. Without even mentioning the other large amount of libraries that python has. Everything else is horrible about python.

## Configuration

For functional execution append the directory of [helpers](./Helpers/) to the PYTHONPATH env variable

Configuration should be located in `/etc/SMB/config.json` with email logging options strictly environment variables

Environment variables:

Email logging (if enabled in `config.json`)

*SMB_LOGGING_EMAIL* -> Sender email

*SMB_LOGGING_EMAIL_PASSWORD* -> Sender email password

*SMB_LOGGING_EMAIL_TARGET* -> Receiver of emails
