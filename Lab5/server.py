import json
import os
import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Loopback address for localhost
PORT = 8080  # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")


# Function to handle a client's messages
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        receivedMessage = json.loads(message)
        print(f"Received from {client_address}: {message}")
        for client in clients:
            serverPath = "media/server/"
            if client_socket == client:
                if receivedMessage["type"] == "connect":
                    sendMessage = {
                        "type": "connect_ack",
                        "payload": {
                            "message": "Connected to the room."
                        }
                    }
                    client.send(json.dumps(sendMessage["payload"]["message"]).encode('utf-8'))
                elif receivedMessage["type"] == "download":
                    if os.path.exists(serverPath + receivedMessage["payload"]["file"]):
                        file = open(serverPath + receivedMessage["payload"]["file"], "rt")
                        contents = file.read()
                        file.close()
                        sendMessage = {
                            "type": "download_ack",
                            "payload": {
                                "file": contents,
                                "fileName": receivedMessage["payload"]["file"]
                            }
                        }
                        client.send(json.dumps(sendMessage).encode('utf-8'))
                    else:
                        client.send(("File " + "'" + receivedMessage["payload"]["file"] + "'" + " doesn't exist").encode('utf-8'))
            else:
                if receivedMessage["type"] == "connect":
                    notification = {
                        "type": "notification",
                        "payload": {
                            "message": receivedMessage["payload"]["name"] + " has joined the room."
                        }
                    }
                    client.send(json.dumps(notification["payload"]["message"]).encode('utf-8'))
                elif receivedMessage["type"] == "message":
                    sendMessage = {
                        "type": "message",
                        "payload": {
                            "name": receivedMessage["payload"]["name"],
                            "room": receivedMessage["payload"]["room"],
                            "text": receivedMessage["payload"]["text"]
                        }
                    }
                    client.send(json.dumps(sendMessage["payload"]["name"] + ": " + sendMessage["payload"]["text"]).encode('utf-8'))
                elif receivedMessage["type"] == "upload":
                    f = open(serverPath + receivedMessage["payload"]["fileName"], "w")
                    f.write(receivedMessage["payload"]["file"])
                    f.close()
                    client.send((receivedMessage["payload"]["name"] + " uploaded a file " + receivedMessage["payload"]["fileName"]).encode('utf-8'))
    clients.remove(client_socket)
    client_socket.close()


clients = []
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    # Start a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
