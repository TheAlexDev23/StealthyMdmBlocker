from mitmproxy import http

from Logger import Logger

logger = Logger()


def request(flow: http.HTTPFlow) -> None:
    if "jamfcloud" in flow.request.pretty_url:
        logger.log(
            f"Request ({flow.request.method} {flow.request.pretty_url})",
            f"Headers: {flow.request.headers}\n"
            + f"Request to with content: \n{flow.request.content}",
        )


def response(flow: http.HTTPFlow) -> None:
    if "jamfcloud" in flow.request.pretty_url:
        assert flow.request
        assert flow.response
        logger.log(
            f"Request ({flow.request.method} {flow.request.pretty_url})",
            f"Headers: {flow.request.headers}\n"
            + f"Request to with content: \n{flow.response.content}",
        )
