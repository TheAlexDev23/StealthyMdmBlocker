# Stealthy MDM Blocker

My attempt at silently blocking mdm functionality. Reverse engineered findings of the mdm functionality can be found [here](./ReverseEngineering/Findings/).

Thep revious solution was essentially a MITM proxy with custom CA certificates that can decrypt and modify outgoing requests and incoming responses to the mdm server. The main solution found [here](./ProfileModification/), is able to differentiate the possible messages that can happen between the client and the server, decode the mdm configuration, modify it to remove most of the restrictions and encode it back again.

Given that a custom CA certificate could be installed in the ios system without restrictions then the modification could not be noticed by the server nor the enrolled device.

The second solution, [here](./RequestBlocking), is a custom DNS that forwards all requests to another DNS of choice except for query requests for the MDM server, those would receive a not found response, and the DNS server would pretend to be the device and communicate with the MDM server itself. Once the communication is finished and the DNS server had pretended to have installed all profiles and restrictions the MDM server had sent it, the DNS on the iOS device could be removed. However, the device believes that the connection with the MDM server failed, and would retry as soon as possible. But given that the DNS server already pretended to be the device, the MDM server would send an empty response due to the lack of commands to execute as all have been "executed" by the DNS server.

## Configuration

For functional execution append the directory of [helpers](./Helpers/) to the PYTHONPATH env variable

Configuration should be located in `/etc/SMB/config.json` with email logging options strictly environment variables

Environment variables:

Email logging (if enabled in `config.json`)

*SMB_LOGGING_EMAIL* -> Sender email

*SMB_LOGGING_EMAIL_PASSWORD* -> Sender email password

*SMB_LOGGING_EMAIL_TARGET* -> Receiver of emails
