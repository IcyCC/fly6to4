import asyncio
from public.logger import log


class Fly6to4Client():


    loop = None
    host = ''
    port = ''


    @classmethod
    async def send_data(cls, msg):
        reader, writer = await asyncio.open_connection(
                        cls.host, cls.port, loop=cls.loop
                        )
        log.info("Client connection host: {} ,port: {} ".format(
            cls.host, cls.port
        ))

        writer.write(msg)
        await writer.drain()
        log.info("Client write mesg :{}".format(str(msg)))
        data = await reader.read(-1)

        log.info("Client receive resp {}".format(str(data)))
        # resp = b''
        # while data:
        #     resp = resp + data
        #     data = await self.reader.read(1024)

        # log.info("Client finish receive resp {}".format(str(resp)))
        writer.close()
        return data
