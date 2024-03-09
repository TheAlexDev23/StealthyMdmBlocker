from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" in flow.request.pretty_url and "checkin" in flow.request.pretty_url:
        flow.response.content = b"Modified content for jamfcloud domain"
