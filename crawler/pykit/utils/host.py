

import netifaces
import ipaddress
from urllib import parse


def get_interface_ip():
    interfaces = netifaces.interfaces()

    for i in interfaces:
        ifaddresses = netifaces.ifaddresses(i)
        if netifaces.AF_INET not in ifaddresses:
            continue

        for j in ifaddresses[netifaces.AF_INET]:
            ip = j['addr']  # should print "192.168.100.37"
            ip_addr = ipaddress.ip_address(ip)

            if not (ip_addr.is_unspecified
                    or ip_addr.is_loopback
                    or ip_addr.is_multicast
                    or ip_addr.is_link_local):
                return ip


def extract(addr: str):

    if addr and (addr != "0.0.0.0" and addr != "[::]" and addr != "::"):
        return addr

    return get_interface_ip()


def parse_address(address: str, scheme: str) -> parse.ParseResult:
    """解析 ip:port 的 url

    Args:
        address (str): ip:port

    Returns:
        parse.ParseResult: 
    """
    if '//' not in address:
        address = f'http://{address}'
    url_parsed = parse.urlparse(address)
    address = extract(url_parsed.hostname)
    port = url_parsed.port
    netloc = f'{address}:{port}'
    endpoint = parse.ParseResult(scheme=scheme, netloc=netloc, query='isSecure=false',
                                 path='', params='', fragment='')
    return endpoint
