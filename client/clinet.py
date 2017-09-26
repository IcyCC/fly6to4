import asyncio
from public.logger import log


class Fly6to4Client():

    def __init__(self, host, port, loop):
        self.loop = loop
        self.host = host
        self.port = port
        self.writer = None
        self.reader = None

    async def connection(self):
        self.reader, self.writer = await asyncio.open_connection(
                        self.host, self.port,loop=self.loop
                        )
        log.info("Client connection host: {} ,port: {} ".format(
            self.host, self.port
        ))

    async def send_data(self, msg):
        if self.writer is None and self.reader is None:
            await self.connection()
        self.writer.write(msg)
        log.info("Client write mesg :{}".format(str(msg)))
        data = await self.reader.read(100)
        resp = b''
        while data is not None:
            resp = resp + data
            data = await self.reader.read(100)

        log.info("Client receive resp {}".format(str(resp)))
        return resp
