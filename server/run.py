import asyncio
from server.servers import Fly4to6Server
from public.logger import log
import uvloop
import logging

if __name__ == '__main__':

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop.set_debug(True)
    logging.getLogger('').setLevel(logging.DEBUG)
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
