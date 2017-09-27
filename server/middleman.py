import asyncio
from public.logger import log

class Middleman:

    @classmethod
    async def forwards(cls, message, loop):
        reader, writer = await asyncio.open_connection(message.get("ip"),
                                                       message.get("port"),
                                                       loop=loop
                                                       )
        writer.write(message.get('data'))
        log.debug("Send to public len: {}".format((message.get("ip"),message.get("port"))))

        await writer.drain()

        data = await reader.read(-1)
        # resp = b''
        # while data:
        #     resp = resp + data
        #     data = await reader.read(100)

        log.debug("Recive from public len:{} ".format(str(len(data))) )

        writer.close()

        return data
