import socket

# Server Configuration
HOST = "0.0.0.0"
PORT = 12345

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable/Disable Nagle’s Algorithm
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)  # Change to 1 to disable

server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[*] Listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"[*] Connection received from {addr}")

with open("received_file.txt", "wb") as f:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)

conn.close()
server_socket.close()
print("[*] File transfer complete.")
