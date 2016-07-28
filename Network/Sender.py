def sendTransaction(ip_address, transaction):
    from socket import *
    port = 2001
    buf_size = 4000
    receiver_addr = (ip_address, port)
    tcp_socket =socket(AF_INET, SOCK_STREAM)
    connected = tcp_socket.connect(receiver_addr)
    if connected is False :
        print "Connection failed to "+ip_address

    else :
        if tcp_socket.send(transaction) is False:
            print "Send fail to "+ip_address

    tcp_socket.close()

def send( transaction):
    for addr in address_list:
        sendTransaction(addr, transaction)

