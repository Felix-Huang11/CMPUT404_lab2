import socket, time, sys
from multiprocessing import Process

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024
host = 'www.google.com'
port = 80

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to google and send response to client
def handle_request(conn, addr, proxy_end):
	send_full_data = conn_recv(BUFFER_SIZE)
	print(f"Sending received data to google")
	proxy_end.sendall(send_full_data)
	proxy_end.shutdown(socket.SHUT_WR)

	data = proxy_end.recv(BUFFER_SIZE)
	print("Sending received data to to client")
	conn.send(data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    	print("Starting proxy server")
    
        #allow reused address
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        while True:
        	#connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
            	print("Connecting to Google")
            	remote_ip = get_remote_ip(host)

            	#connect proxy_end
            	proxy_end.connect(remote_ip, port)

            	#allow for multiple connections with a process daemon
            	p = Process(target = handle_request, args=(conn, addr, proxy_end))
            	p.daemon = True
            	p.start()
            	print("started process", p)
            conn.close()

if __name__ == "__main__":
    main()