def start(thread_name, ip_address):
    from socket import *
    from DataStorage import FileController
    port = 2001
    addr = (ip_address,port)
    buf_size = 4000

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind(addr)
    tcp_socket.listen(5)
    print "Receiver is started"

    while True:
        receive_socket, sender_ip = tcp_socket.accept()
        print "\nTransaction received from ", sender_ip
        print ">"

        while True:
            data = receive_socket.recv(buf_size)
            if len(data) > 1:
                FileController.add_transaction(data)
                break

    tcp_socket.close()
    receive_socket.close()