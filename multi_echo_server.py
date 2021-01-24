#!/usr/bin/env python3
import socket
from multiprocessing import Process

# CONSTANTS
INBOUND_HOST = "" # Listen for all possible hosts
INBOUND_PORT = 8001
INBOUND_BUFFER_SIZE = 1024

def echo(conn, addr):
    print("Connected by:", str(addr[0]) + ":" + str(addr[1]))
    with conn:
        # Accepted connection
        data = conn.recv(INBOUND_BUFFER_SIZE)
        conn.sendall(data)
        conn.shutdown(socket.SHUT_RDWR)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        # Set socket option, here, reuse the same bind port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to address
        s.bind((INBOUND_HOST, INBOUND_PORT))

        # Set to listening mode
        s.listen(2)

        # Continuously listen for connections
        while True:
            conn, addr = s.accept()
            p = Process(target=echo, args=(conn, addr))
            p.daemon = True
            p.start()
            print("Start process:", p.pid)

if __name__ == "__main__":
    main()