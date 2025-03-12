import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))  # Bind to all interfaces
    server_socket.listen(100)  # Backlog queue

    print("[*] Server is listening on port 8080...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[*] Connection accepted from {addr}")
        
        data = conn.recv(1024)  # Read up to 1024 bytes
        if data:
            print(f"[*] Received data: {data.decode(errors='ignore')}")
        
        conn.close()

if __name__ == "__main__":
    main()
