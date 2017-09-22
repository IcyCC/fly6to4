import asyncio
from .server import Fly4to6Server
from public.logger import log

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    local_server = loop.create_server(lambda : Fly4to6Server(loop=loop),
                                      host='127.0.0.1',
                                      port=8080)
    server = loop.run_until_complete(local_server)

    try:
        log.info("Server start at port : {}".format(8080))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
