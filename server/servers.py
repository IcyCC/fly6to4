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

    def __init__(self, loop: asyncio.BaseEventLoop):
        self.transport = None
        self.loop = loop
        self.parser = None
        self.headers = []
        self.data = b''
        self.resolver = aiodns.DNSResolver(loop=asyncio.get_event_loop(), rotate=True)

    resp = b''

    @classmethod
    def set_resp_value(cls, data, body):
        if data is None:
            return
        cls.resp = data[0][0]
        msg = Parser.http_parser(cls.resp, 80, body)
        print(msg)

    def connection_made(self, transport):
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))

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
                                add_done_callback(functools.partial(get_resp, body=self.data))
        print(self.resp)


def get_resp(fu, body):
    Fly4to6Server.set_resp_value(fu.result(), body)
