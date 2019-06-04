import socket

class Sender:
    def __init__(self, port=37020):
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        self._sock.settimeout(0.2)
        self._sock.bind(("", 44444))

    def send(self, msg):
        self._sock.sendto(msg, ('<broadcast>', self.port))