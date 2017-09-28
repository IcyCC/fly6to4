import asyncio
import httptools
import struct
import functools
from server.middleman import Middleman
from public.parser import Parser
from public.logger import log
from public import constants
from public import error
import socket


class Client(asyncio.Protocol):

    def __init__(self):
        self.connected = False
        self.transport = None

    def connection_made(self, transport):
        self.connected = True
        self.transport = transport

    def data_received(self, data):
        log.debug(" server midlleman receive data with length {}".format(len(data)))
        self.transport.write(data)

    def connection_lost(self, *args):
        self.connected = False
        self.transport.close()


class Fly4to6Server(asyncio.Protocol):

    def __init__(self, loop: asyncio.BaseEventLoop):
        self.transport = None
        self.loop = loop
        self.data = b''
        self.stage = constants.Stage_NULL
        self.method = 0
        self.waiter = None
        self._client = None


    def connection_made(self, transport):
        log.info('Connection from {}'.format(
            transport.get_extra_info('peername')))
        self.transport = transport
        self.stage = constants.STAGE_HELLO

    def data_received(self, data):
        if self.stage == constants.STAGE_HELLO:
            ver, nmethods = struct.unpack('!BB', data[0:2])
            if ver != 5:
                raise error.NotRecognizeProtocolException('Unsuport')
            methods = struct.unpack('!'+'B' * nmethods, data[2:2 + nmethods])

            if constants.METHOD_USER in methods:
                self.method = constants.METHOD_USER
            elif constants.METHOD_NOAUTH in methods:
                self.method = constants.METHOD_NOAUTH
            else:
                self.method = constants.METHOD_NOAC
            resp = b'\x05' + struct.pack('!B', self.method)
            log.info("HELLO FINISH")
            self.transport.write(resp)

            if self.method == constants.METHOD_NOAC:
                self.transport.close()
                log.info("No available auth method !")
                return

            if self.method == constants.METHOD_NOAUTH:
                self.stage = constants.STAGE_INIT
            else:
                self.stage = constants.STAGE_AUTH

        elif self.stage == constants.STAGE_AUTH:
            log.info("AUTH FINISH")
            self.auth(data)

        elif self.stage == constants.STAGE_INIT:
            ver, cmd, rsv, atyp = struct.unpack('!BBBB', data[0:4])

            log.info("INIT FINISH")

            if cmd == constants.SOCKS_CMD_CONNECT:
                domain, port = self.parse_connect(atyp,data)
                self.waiter = asyncio.ensure_future(self.cmd_connect(domain, port))
                self.stage = constants.STAGE_WORK
                log.info("connect to {}, {}".format(domain, port))

            elif cmd == constants.SOCKS_CMD_BIND:
                pass
            else:
                raise NotImplementedError("Not implement {} yet!".format(cmd))

        elif self.stage == constants.STAGE_WORK:
            log.debug("send data with length {}".format(len(data)))
            asyncio.ensure_future(self.send_data(data))
        else:
            raise Exception("Unknown stage")

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.transport.close()
        if hasattr(self, '_client'):
            self._client.transport.close()

    def auth(self, data):
        self.transport.write(b'\x01\x00')

    def parse_connect(self, atyp, data):
        cur = 4
        if atyp == constants.SOCKS5_ATYP_DOMAIN:
            domain_len = struct.unpack('!B', data[cur:cur + 1])[0]
            cur += 1

            domain = data[cur:cur + domain_len].decode()
            cur += domain_len

        elif atyp == constants.SOCKS5_ATYP_IPv4:
            domain = socket.inet_ntop(socket.AF_INET, data[cur:cur + 4])
            cur += 4

        elif atyp == constants.SOCKS5_ATYP_IPv6:
            domain = socket.inet_ntop(socket.AF_INET6, data[cur:cur + 16])
            cur += 16

        else:
            raise Exception("Unknown address type")

        port = struct.unpack('!H', data[cur:cur+2])[0]

        return domain, port

    async def cmd_connect(self, domain, port):
        transport, client = await self.loop.create_connection(Client, domain, port)
        client.server_transport = self.transport
        self._client = client
        ip, port = transport.get_extra_info('sockname')

        resp = b'\x05\x00\x00\x01'
        for i in ip.split('.'):
            resp += struct.pack('!B', int(i))
        resp += struct.pack('!H', port)
        self.transport.write(resp)
        log.debug("Server connected to {}, {}".format(domain, port))

    async def send_data(self, data):
        await self.waiter
        self._client.transport.write(data)


