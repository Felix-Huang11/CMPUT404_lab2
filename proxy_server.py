#!/usr/bin/env python3
import socket

# CONSTANTS
HOST = "" # Listen for all possible hosts
PORT = 8001
BUFFER_SIZE = 1024
host = "www.google.com"
port = 80

def main():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        # Set socket options, here, reuse the same bind port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to address
        s.bind((HOST, PORT))
        
        # Set to listening mode
        s.listen(2)
        
        # Continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by:", str(addr[0]) + ":" + str(addr[1]))
            
            # Accepted connection
            with conn:
                # Fetch data from client
                client_data = conn.recv(BUFFER_SIZE)
                # Then send the client data to the target server
                # Create a socket object
                print("Received From:", str(addr[0]) + ":" + str(addr[1]), "Content:", client_data)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_s:
                    # Connect to the target server
                    proxy_s.connect((socket.gethostbyname(host), port))
                    print("Connecting to:", socket.gethostbyname(host) + ":" + str(port))
                    proxy_s.sendall(client_data)
                    proxy_data = b""
                    while True:
                        fetched_data = proxy_s.recv(BUFFER_SIZE)
                        if not fetched_data:
                            break
                        proxy_data += fetched_data
                    peer_addr = proxy_s.getpeername()
                    print("Response from:", str(peer_addr[0]) + ":" + str(peer_addr[1]), "Content:", proxy_data)
                    conn.sendall(proxy_data)

if __name__ == "__main__":
    main()