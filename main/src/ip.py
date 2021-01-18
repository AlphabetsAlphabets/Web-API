def host():
    import socket

    return socket.gethostbyname(socket.gethostname())
