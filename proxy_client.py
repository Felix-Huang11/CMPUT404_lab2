#!/usr/bin/env python3
import socket

# CONSTANTS
HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 1024
PAYLOAD_URL = "www.google.com"
PAYLOAD = f"GET / HTTP/1.0\r\nHost: {PAYLOAD_URL}\r\n\r\n"

def main():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Connect to the proxy server
        s.connect((HOST, PORT))

        # Send the payload to the proxy server
        s.sendall(PAYLOAD.encode())

        # Get IP and port of peer
        peer_addr = s.getpeername()

        # No longer write/send
        s.shutdown(socket.SHUT_WR)

        # Reading data until no more left
        data = b""
        while True:
            fetched_data = s.recv(BUFFER_SIZE)
            if not fetched_data:
                break
            data += fetched_data

        print("Received From:", str(peer_addr[0]) + ":" + str(peer_addr[1]), "Content:", data)

if __name__ == "__main__":
    main()