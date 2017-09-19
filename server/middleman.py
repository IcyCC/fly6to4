import asyncio
from public.logger import log

class Middleman:

    def __init__(self, loop):
        self.loop = loop

    async def forwards(self, message):
        reader, writer = await asyncio.open_connection(message.get("ip"),
                                                       message.get("port"),
                                                       self.loop
                                                       )
        writer.write(message.encode())
        log.debug("Send to public len: {}".format(str(len(message))))

        data = await reader.read(100)
        resp = b''
        while data is not None:
            resp = resp + data
            data = await reader.read(100)

        log.debug("Recive from public len:{} ".format(str(len(message))) )

        writer.close()

        return resp