#!/usr/bin/python3

import socket
import os

CHUNK_SIZE = 1024  # 1KB

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            client_socket.sendall(chunk)
    client_socket.sendall(b'END')  # Indicate end of file transfer

def receive_file(client_socket, file_name):
    with open(file_name, 'wb') as file:
        while True:
            chunk = client_socket.recv(CHUNK_SIZE)
            if chunk == b'END':
                break
            file.write(chunk)

def client():
    host = socket.gethostname()
    port = 4242

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connection Successful")

    while True:
        message = input("> ")

        if message == "push":
            file_path = input("Enter the file path to upload: ")
            if os.path.exists(file_path):
                client_socket.sendall(f"push {os.path.basename(file_path)}".encode())
                send_file(client_socket, file_path)
            else:
                print("File does not exist.")

        elif message == "pull":
            file_name = input("Enter the file name to download: ")
            client_socket.sendall(f"pull {file_name}".encode())
            receive_file(client_socket, file_name)

        elif message == "exit":
            client_socket.sendall("exit".encode())
            break

    client_socket.close()

if __name__ == "__main__":
    client()
