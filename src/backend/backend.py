import json
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    data = client_socket.recv(1024)

    if data:
        message = json.loads(data.decode())
        print(f"Received message: {message}")

    client_socket.close()
