import socket

def socket_receive(socket_file):
    data = socket_file.readline()
    print(data, end="")
    return data

def socket_send(socket_file, message):
    socket_file.write(message+"\n")
    socket_file.flush()
    print(message)

def main():
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    server_socket.bind((socket.gethostname(), 12345)) # cl3.learner.csie.ntu.edu.tw
    # become a server socket
    server_socket.listen(5)

    while True:
        # accept connections from outside
        client_socket, address = server_socket.accept()
        # now do something with the client_socket
        # in this case, we'll pretend this is a threaded server
        # ct = client_thread(client_socket)
        # ct.run()

        print("Got connection from", address)
        client_socket_file = client_socket.makefile("rw")
        socket_send(client_socket_file, "Thank you for connecting")
        # client_socket.send("Thank you for connecting")
        # client_socket.close()     
        client_socket_file.close()
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()

if __name__ == "__main__":
    main()