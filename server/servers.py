import asyncio
from server.middleman import Middleman
from public.parser import Parser
from public.logger import log


class Fly4to6Server(asyncio.Protocol):

    def __init__(self, loop):
        self.transport = None
        self.middleman = Middleman(loop)
        self.loop = loop

    def connection_made(self, transport):
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))

        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        # message = Parser.tcp_parser(message)
        resp = self.middleman.forwards(message)

        self.transport.write(resp)
        self.transport.close()
