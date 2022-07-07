""" Edit a HTTP header.

    When connecting using the socket, the OS might not be able to resolve the name, in this case
    use an online look-up for the IP.
    
    Script reads in a HTTP header from a file and prepares it i.e. ensures delimiters are carriage
    return and new lines.

    On receiving data, the data is checked for the byte code \x1f\x8b which is the first two bytes
    of a gzip compressed byte object, it then proceeds to decompress ready for decoding.
"""
import socket
import gzip

def is_gzip_encoded(bytes_obj):
    """ Creates a new list while checking each line for gzip compressed data.
        If found, decompress using gzip module and append to new list. 
    """
    bytes_split = bytes_obj.split(b'\r\n')
    
    bytes_list = []
    for byte_line in bytes_split:

        if byte_line.startswith(b'\x1f\x8b'):
            decoded = gzip.decompress(byte_line)
            bytes_list.append(decoded)
            continue
        
        bytes_list.append(byte_line)

    return b''.join(bytes_list)


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

        self.byte_data_decompress = is_gzip_encoded(self.byte_data)

        self.string_data = self.byte_data_decompress.decode('utf-8')

        return self.string_data


# Open a file which contains HTTP header and prepares it.
with open('HTTP_header.txt', 'r') as file:

    file_lines = file.readlines()

    stripped_list = []

    for line in file_lines:

        stripped_list.append(line.rstrip().rstrip('\r'))

    prepared_header_string = '\r\n'.join(stripped_list)

    prepared_header_string += '\r\n\r\n'

    

header = prepared_header_string

control_obj = HttpSocket(host= '176.9.9.172', header=header)

control_obj.connect()

control_obj.send()

control_obj.receive()

data = control_obj.decode()

print(data)