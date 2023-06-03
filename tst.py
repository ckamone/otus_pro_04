# python3
import socket
import sys
import time

# 1 run_server - запуск сервер
# 1.1 create_serv_sock - биндимся сокет

DEBUG = True

def run_server(port=8080):
    '''запуск сервера'''
    if DEBUG:
        print('run_server')
    # биндим порт
    serv_sock = create_serv_sock(port)
    cid = 0
    while True:
        # принимаем клиента
        client_sock = accept_client_conn(serv_sock, cid)
        # обслуживаем клиента
        serve_client(client_sock, cid)
        cid += 1


def create_serv_sock(serv_port):
    '''биндим порт'''
    if DEBUG:
        print('create_serv_sock')
    # с помощью socket создаем объект для работы с сокетом
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              proto=0)
    # биндимся и слушаем сокет
    serv_sock.bind(('0.0.0.0', serv_port))
    serv_sock.listen()
    print('Listening on {}:{}'.format('127.0.0.1', serv_port))
    return serv_sock


def accept_client_conn(serv_sock, cid):
    '''принимаем клиента'''
    if DEBUG:
        print('accept_client_conn')
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock
    

def serve_client(client_sock, cid):
    '''обслуживаем клиента'''
    if DEBUG:
        print('serve_client')
    # читаем запрос
    request = read_request(client_sock)
    print('Received {}'.format(request))
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        # задерживаем запрос
        response = handle_request(request)
        # выдача ответа 
        write_response(client_sock, response, cid)


def read_request(client_sock, delimiter=b'\r\n\r\n'):
    '''читаем запрос'''
    if DEBUG:
        print('read_request')
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(4)
            if not chunk:
                # Клиент преждевременно отключился.
                return None

            request += chunk
            if delimiter in request:
                return request

    except ConnectionResetError:
        # Соединение было неожиданно разорвано.
        return None
    except:
        raise


def handle_request(request):
    '''удерживаем запрос'''
    if DEBUG:
        print('handle_request')
    #time.sleep(5)
    #return request[::-1]
    responce = 'HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/6.0\r\nContent-Type: text/html\r\n\r\n'
    if 'HEAD' in request.decode():
        return responce
    elif 'GET' in request.decode():
        return responce + '<html><pre>{0}</pre></html>'
    else:
        return 'HTTP/1.1 400 Bad request\r\nServer: Microsoft-IIS/6.0\r\nContent-Type: text/html\r\n\r\n'



def write_response(client_sock, response, cid):
    '''выдаем ответ'''
    if DEBUG:
        print('write_response')
    client_sock.sendall(response.encode())
    client_sock.close()
    print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))