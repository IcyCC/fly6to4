import asyncio
import functools
from client.clinet import Fly6to4Client
from public.logger import log
from struct import pack, unpack



class Fly4to6local(asyncio.Protocol):

    def __init__(self, loop, host, port, connections=None):
        self.transport = None
        self.loop = loop
        self.host = host
        self.port = port
        if connections is None:
            connections = dict()
        self.connections = connections
        Fly6to4Client.host = host
        Fly6to4Client.port = port
        Fly6to4Client.loop = loop

    def connection_made(self, transport):
        self.connections[self] = True
        self.transport = transport
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))

    def data_received(self, data):
        message = data
        log.info("Local recive data {} ".format(str(message)))
        func = functools.partial(send_2_local, transport=self.transport)
        asyncio.ensure_future(Fly6to4Client.send_data(message),loop=self.loop).add_done_callback(func)

    def connection_lost(self, exc):
        log.info('Local server closed the connection')
        log.info('Stop the event loop')

def send_2_local(fu, transport):
    transport.write(fu.result())
    log.debug("send2local")
    transport.write_eof()
