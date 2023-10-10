import socket
import threading
import json
import os

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 8080  # Server's port
# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


# Function to receive and display messages
def receive_messages():
    while True:
        receivedMessage = client_socket.recv(1024).decode('utf-8')
        if not receivedMessage:
            break
        try:
            receivedMessage = json.loads(receivedMessage)
            clientFile = open("media/client/" + receivedMessage["payload"]["fileName"], "wt")
            clientFile.write(receivedMessage["payload"]["file"])
            clientFile.close()
            print(f"\nSaved {receivedMessage['payload']['fileName']} in media/client/")
        except:
            print(f"\nReceived: {receivedMessage}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()
username = input("Enter your name: ")
userRoom = input("Enter your room: ")
connectMessage = {
    "type": "connect",
    "payload": {
        "name": username,
        "room": userRoom
    }
}

jsonConnectMessage = json.dumps(connectMessage)
client_socket.send(jsonConnectMessage.encode('utf-8'))
while True:
    message = input("Enter a message/command; Available commands('U'-upload, 'D'-download, 'exit'-quit): ")
    if message.lower() == 'exit':
        break
    elif message.lower() == 'u':
        while True:
            filePath = input("Enter the file path to upload: ")
            if os.path.exists(filePath):
                if os.path.isfile(filePath):
                    break
                else:
                    print(f"Path: '{filePath}' is not a file. Please enter a valid file path.")
            else:
                print(f"Path: '{filePath}' doesn't exist. Please enter a valid file path.")
        file = open(filePath, "rt")
        contents = file.read()
        file.close()
        sendMessage = {
            "type": "upload",
            "payload": {
                "name": username,
                "room": userRoom,
                "file": contents,
                "fileName": os.path.basename(filePath)
            }
        }
        sendMessage = json.dumps(sendMessage)
        client_socket.send(sendMessage.encode('utf-8'))
    elif message.lower() == 'd':
        file = input("Enter the file name.extension to download: ")
        sendMessage = {
            "type": "download",
            "payload": {
                "name": username,
                "room": userRoom,
                "file": file
            }
        }
        sendMessage = json.dumps(sendMessage)
        client_socket.send(sendMessage.encode('utf-8'))
    else:
        sendMessage = {
            "type": "message",
            "payload": {
                "name": username,
                "room": userRoom,
                "text": message
            }
        }
        message = json.dumps(sendMessage)
        client_socket.send(message.encode('utf-8'))
client_socket.close()
