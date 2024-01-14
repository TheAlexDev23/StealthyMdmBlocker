from mitmproxy import http

from EmailSender import EmailSender

def request(flow: http.HTTPFlow) -> None:
    if "jamfcloud" in flow.request.pretty_url:
        EmailSender.send_email(f"Request ({flow.request.method})", f"Request to {flow.request.pretty_url} with content: \n {flow.request.content}")

def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" in flow.request.pretty_url:
        EmailSender.send_email(f"Response ({flow.request.method})", f"Response from {flow.request.pretty_url} with content: \n {flow.response.content}")
