import asyncio
from public.logger import log


class Fly6to4Client(asyncio.Protocol):

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        log.debug("client send message len: {} to ".format(len(self.message)))

    def data_received(self, data):
        pass
