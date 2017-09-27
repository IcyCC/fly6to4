import asyncio
import httptools
import functools
from server.middleman import Middleman
from public.parser import Parser
from public.logger import log
from public.dns import dns_look_up
import socket
import aiodns


class Fly4to6Server(asyncio.Protocol):

    def __init__(self, loop: asyncio.BaseEventLoop,  connections=None):
        if connections is None:
            connections = dict()
        self.connections = connections
        self.transport = None
        self.loop = loop
        self.parser = None
        self.headers = []
        self.data = b''
        self.resolver = aiodns.DNSResolver(loop=asyncio.get_event_loop(), rotate=True)

    resp = b''

    @classmethod
    def set_resp_value(cls, data, body, loop, transport):
        if data is None:
            return
        cls.resp = data[0][0]
        msg = Parser.http_parser(cls.resp, 80, body)
        print(msg)
        func = functools.partial(send_2_client, transport=transport)
        asyncio.ensure_future(Middleman.forwards(msg, loop=loop), loop=loop).add_done_callback(func)


    def connection_made(self, transport):
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))
        self.connections[self] = True
        self.transport = transport

    def data_received(self, data):
        if self.parser is None:
            self.parser = httptools.HttpRequestParser(self)
        self.data = data
        try:
            self.parser.feed_data(data)
        finally:
            pass

    def on_header(self, name, value):
        self.headers.append((name.decode('utf-8'), value.decode('utf-8')))

    def on_message_complete(self):
        host=''
        for k, v in self.headers:
            if k == 'Host':
                if ':' in v:
                    host, port = v.split(':')
                else:
                    host = v
                    port = 80
        asyncio.ensure_future(self.resolver.query(host=host,
                                                  qtype='A'), loop=self.loop).\
                                add_done_callback(functools.partial(get_resp, body=self.data, loop = self.loop,transport = self.transport))
        print(self.resp)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        del self.connections[self]



def get_resp(fu, body, loop, transport):
    Fly4to6Server.set_resp_value(fu.result(), body, loop, transport)


def send_2_client(fu, transport):
    log.info("Server feed back to client h")
    transport.write(fu.result())