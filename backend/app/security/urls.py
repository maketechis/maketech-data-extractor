import ipaddress
import socket
from urllib.parse import urlparse

BLOCKED_HOSTS={"localhost","localhost.localdomain"}

def validate_public_http_url(url:str)->str:
    parsed=urlparse(url)
    if parsed.scheme not in ("http","https") or not parsed.hostname:
        raise ValueError("Only public HTTP(S) URLs are allowed")
    host=parsed.hostname.lower().rstrip(".")
    if host in BLOCKED_HOSTS or host.endswith(".local"):
        raise ValueError("Local hosts are not allowed")
    try:
        infos=socket.getaddrinfo(host,parsed.port or (443 if parsed.scheme=="https" else 80),type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError("Hostname could not be resolved") from exc
    for info in infos:
        ip=ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError("Private, loopback, link-local, reserved or non-global addresses are not allowed")
    return url
