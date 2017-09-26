
class Parser:

    @classmethod
    def tcp_parser(cls, data):
        return {
            "ip": "",
            "port": "",
            "data": data
        }

    @classmethod
    def http_parser(cls, ip, port, data):
        return {
            "ip": ip,
            "port": port,
            "data": data
        }
