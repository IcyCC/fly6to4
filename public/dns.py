import asyncio
import aiodns
import socket


def dns_look_up(host, port):

    res = socket.getaddrinfo(host, port)
    if res is not None:
        return res[0][4]
    return None
