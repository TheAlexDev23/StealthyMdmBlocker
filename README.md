# StealthyMdmBlocker

My attempt at silently blocking mdm functionality. Reverse engineered findings of the mdm functionality can be found [here](./ReverseEngineering/Findings/).

The current solution is essentially a MITM proxy with custom CA certificates that can decrypt and modify outgoing requests and incoming responses to the mdm server. The main solution found [here](./RequestModification/), is able to differentiate the possible messages that can happen between the client and the server, decode the mdm configuration, modify it to remove most of the restrictions and encode it back again.

It's written in python because mitmproxy (my MITM proxy of choice) only has request/response editing modules for python. Without even mentioning the other large amount of libraries that python has. Everything else is horrible about python.

## Configuration

Email logging (if enabled)

*MDM_MITMPROXY_NOTIFIER_EMAIL_SEND* -> Sender Email
*MDM_MITMPROXY_NOTIFIER_EMAIL_SEND_PSWD* -> Sender Password
*MDM_MITMPROXY_NOTIFIER_EMAIL_RECEIVE* -> Receiver Email
