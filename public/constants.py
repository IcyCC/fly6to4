Stage_NULL = 0
STAGE_HELLO = 1
STAGE_AUTH = 2
STAGE_INIT = 3
STAGE_WORK = 4

METHOD_NOAUTH = 0
METHOD_USER = 2
METHOD_NOAC = 0xFF

SOCKS5_ATYP_IPv4 = 1
SOCKS5_ATYP_DOMAIN = 3
SOCKS5_ATYP_IPv6 = 4

RSV = NULL = 0
SOCKS_VER5 = 5

SOCKS_CMD_CONNECT = 1
SOCKS_CMD_BIND = 2
SOCKS_CMD_UDP_ASSOCIATE = 3




SOCKS5_ERRORS = {
    0x01: 'General SOCKS server failure',
    0x02: 'Connection not allowed by ruleset',
    0x03: 'Network unreachable',
    0x04: 'Host unreachable',
    0x05: 'Connection refused',
    0x06: 'TTL expired',
    0x07: 'Command not supported, or protocol error',
    0x08: 'Address type not supported'
}
