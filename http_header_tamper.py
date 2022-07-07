""" Edit a HTTP header.

    When connecting using the socket, the OS might not be able to resolve the name, in this case
    use an online look-up for the IP.
    Decode method might throw an exception of bytes not recognised, check the encoding e.g. if the bytes
    are compressed using gzip etc, then the body needs to be decompressed using gzip.decompress(data) for
    example.
"""
import socket


class HttpSocket():

    def __init__(self, host, header='', http_sock=None):

        self.BUFF_SIZE = 4096
        self.host = host
        self.port = 80
        self.header = header
        self.chunks = []
        if http_sock == None:
            self.http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.http_sock = http_sock

    
    def connect(self):
        print('Connecting to socket ...')
        self.http_sock.connect((self.host, self.port))
        print('Socket connected ...')

    
    def send(self):
        total_sent = 0

        self.header_bytes = self.header.encode('utf-8')

        while total_sent < len(self.header_bytes):
            sent = self.http_sock.send(self.header_bytes[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken.")
            total_sent += sent

        
    
    def receive(self):
        self.chunks = []

        print('Starting data received ...')
        while True:
            data = self.http_sock.recv(self.BUFF_SIZE)
            self.chunks.append(data)
            if len(data) < self.BUFF_SIZE: break
        
        print('Data received ...')

    def decode(self):
        self.byte_data = b''.join(self.chunks)

        print(self.byte_data)
        self.string_data = self.byte_data.decode('utf-8')

        return self.string_data



header = """GET / HTTP/1.1\r\nHost: natas0.natas.labs.overthewire.org\r\n\r\n"""


control_obj = HttpSocket(host= '176.9.9.172', header=header)

control_obj.connect()

control_obj.send()

control_obj.receive()

data = control_obj.decode()

print(data)