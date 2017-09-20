import asyncio
from client.clinet import Fly6to4Client
from public.logger import log



class Fly4to6local(asyncio.Protocol):

    def __init__(self,loop:asyncio.BaseEventLoop, host, port):
        self.transport = None
        self.loop = loop
        self.host = host
        self.port = port
        self.client = Fly6to4Client(host=host,
                                    port=port,
                                    loop=loop)

    def connection_made(self, transport):
        self.transport = transport
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))

    def data_received(self, data):
        message = data
        resp = self.loop.run_until_complete(self.client.send_data(message))
        self.transport.write(resp)
        self.transport.close()
