import socket

def listen(data_handler, port=37020, nBytes=1024):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", port))
    while True:
        data, addr = client.recvfrom(nBytes)
        print("received message: %s"%data)
        data_handler(data)