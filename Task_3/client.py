import socket
import time

HOST = "SERVER_IP"  # Change to your server's IP
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable/Disable Nagle’s Algorithm
# client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)  # Change to 1 to disable

client_socket.connect((HOST, PORT))

with open("4kb_file.txt", "rb") as f:
    while (chunk := f.read(40)):  # Send 40 bytes at a time
        client_socket.send(chunk)
        time.sleep(1)  # Control the rate to 40 bytes/sec

client_socket.close()
print("[*] File transfer complete.")
