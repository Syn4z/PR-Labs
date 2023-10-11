import base64
import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


def receive_messages():
    while True:
        receivedMessage = client_socket.recv(4096).decode('utf-8')
        if not receivedMessage:
            break
        try:
            receivedMessage = json.loads(receivedMessage)
            if os.path.splitext(receivedMessage["payload"]["fileName"])[1].lower() == ".png":
                clientFile = open("media/client/" + receivedMessage["payload"]["fileName"], "wb")
                clientFile.write(base64.b64decode(receivedMessage["payload"]["file"]))
                clientFile.close()
            else:
                clientFile = open("media/client/" + receivedMessage["payload"]["fileName"], "wt")
                clientFile.write(receivedMessage["payload"]["file"])
                clientFile.close()
            print(f"\nSaved {receivedMessage['payload']['fileName']} in media/client/")
        except:
            print(f"\nReceived: {receivedMessage}")
        print("Enter a message/command; Available commands('U'-upload, 'D'-download, 'exit'-quit): ")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()


def user_input():
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
            contents = ""
            if os.path.splitext(filePath)[1].lower() == ".txt":
                file = open(filePath, "rt")
                contents = file.read()
                file.close()
            elif os.path.splitext(filePath)[1].lower() == ".png":
                with open(filePath, "rb") as file:
                    contents = base64.b64encode(file.read()).decode('utf-8')
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
            while True:
                file = input("Enter the file name.extension to download: ")
                if file == "":
                    print("Please enter a valid file name.extension")
                else:
                    break
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

user_input_thread = threading.Thread(target=user_input)
user_input_thread.start()
user_input_thread.join()
