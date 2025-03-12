import socket
import threading
import time
import sys

def connect_and_send(server_ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 8080))  # Connect to server
        
        message = b"HelloServer" * 10  # 100 bytes message
        client_socket.sendall(message)
        
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

def main(server_ip):
    while True:
        thread = threading.Thread(target=connect_and_send, args=(server_ip,))
        thread.start()
        time.sleep(1)  # Wait 1 second before starting the next connection

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 legitimate.py <server_ip>")
        sys.exit(1)

    main(sys.argv[1])
