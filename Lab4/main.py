import socket
import signal
import sys
import json
import re

input_file = open('pageInfo.json', 'r')
json_decode = json.load(input_file)
pagesInfo = []
for item in json_decode:
    pageInfo = {'name': item.get('name'), 'author': item.get('author'), 'price': item.get('price'),
                'description': item.get('description')}
    pagesInfo.append(pageInfo)

HOST = '127.0.0.1'
PORT = 8080
pagePath = r'^/product/(\d+)$'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")


def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")
    request_lines = request_data.split('\n')
    if len(request_lines) < 1:
        client_socket.close()
        return
    request_line = request_lines[0].strip().split()
    if len(request_line) < 2:
        client_socket.close()
        return
    path = request_line[1]
    response_content = ''
    status_code = 200
    if path == '/':
        response_content = 'This is the Home page.'
    elif path == '/products':
        for x in range(len(pagesInfo)):
            response_content += f'<a href="product/{x}">Product {x}</a>''<br>'
    elif re.match(pagePath, path):
        for key, value in pagesInfo[int(re.match(pagePath, path).group(1))].items():
            response_content += f'<b> {key} </b> : {value} <br>'
    elif path == '/about':
        response_content = 'This is the About page.'
    elif path == '/contacts':
        response_content = 'This is the Contacts page.'
    else:
        response_content = '404 Not Found'
        status_code = 404
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))
    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        handle_request(client_socket)
    except KeyboardInterrupt:
        pass
