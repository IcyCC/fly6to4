import asyncio
from client.local import Fly4to6local
from public.logger import log

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    local_server = loop.create_server(lambda: Fly4to6local(loop=loop,host="127.0.0.1",port=8080),
                                      host="127.0.0.1",port=1080)
    server = loop.run_until_complete(local_server)

    try:
        log.info("Local start at port : {}".format(1080))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
