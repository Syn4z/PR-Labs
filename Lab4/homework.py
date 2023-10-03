import socket
import re


def parser(path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    request = f'GET {path} HTTP/1.1\r\nHost: 127.0.0.1:8080\r\n\r\n'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response


productContent = parser('/products')
pages = ['/', '/about', '/contacts']
pageContent = []
for page in pages:
    pageResponse = parser(page)
    pageContent.append(re.search(r'\n\n(.*)$', pageResponse).group(1))
productsLinks = re.findall(r'href="product/(\d+)"', productContent)
productInfo = []

for link in productsLinks:
    productPath = f'/product/{link}'
    productContent = parser(productPath)
    productDictionary = {}
    for info in re.findall(r'<b>\s*(.*?)\s*</b>\s*:\s*(.*?)\s*<br>', productContent):
        productDictionary[info[0]] = info[1]
    productInfo.append(productDictionary)

print(f'Simple page contents:\n{pageContent}')
print('\nProduct details dictionaries:')
for dictionary in productInfo:
    print(dictionary)
