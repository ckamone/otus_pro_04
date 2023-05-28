import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))

def method_handler(request):
    responce = 'HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/6.0\r\nContent-Type: text/html\r\n\r\n'
    if 'HEAD' in request.decode():
        return responce
    elif 'GET' in request.decode():
        return responce + '<html><pre>{0}</pre></html>'
    else:
        return 'HTTP/1.1 400 Bad request\r\nServer: Microsoft-IIS/6.0\r\nContent-Type: text/html\r\n\r\n'

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request))

    # TODO какой то метод который будет обрабатывать запрос и выдавать ответ
    http_response = method_handler(request)

    # заглушка
    # http_response = 'HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/6.0\r\nContent-Type: text/html\r\n\r\n<html><pre>{0}</pre></html>'

    client_socket.send(http_response.encode())
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()