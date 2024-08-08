#!/usr/bin/python3

import socket
import os

CHUNK_SIZE = 1024  # 1KB
SAVE_DIR = "server_files"

def save_file(connection_socket, file_name):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    with open(os.path.join(SAVE_DIR, file_name), 'wb') as file:
        while True:
            chunk = connection_socket.recv(CHUNK_SIZE)
            if chunk == b'END':
                break
            file.write(chunk)

def send_file(connection_socket, file_name):
    file_path = os.path.join(SAVE_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                connection_socket.sendall(chunk)
        connection_socket.sendall(b'END')  # Indicate end of file transfer
    else:
        connection_socket.sendall(b'ERROR: File not found')

def server():
    port = 4242
    host = socket.gethostname()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print('The server is ready to receive')

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        while True:
            command = connection_socket.recv(1024).decode().strip()
            if command.startswith("push"):
                _, file_name = command.split()
                save_file(connection_socket, file_name)
            elif command.startswith("pull"):
                _, file_name = command.split()
                send_file(connection_socket, file_name)
            elif command == "exit":
                break

        connection_socket.close()

if __name__ == "__main__":
    server()
