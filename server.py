import socket
from random import randrange
from Crypto.PublicKey import RSA
from Crypto import Random
from hashlib import sha256
from collections import defaultdict

def socket_receive(socket_file):
    data = socket_file.readline()
    print(data, end="")
    return data

def socket_send(socket_file, message):
    socket_file.write(message+"\n")
    socket_file.flush()
    print(message)

class ballot_id_generator():
    def __init__(self):
        self.ballot_ids = set()
    def generate_id(self):
        while True:
            generated_id = randrange(2<<80)
            if generated_id not in self.ballot_ids:
                self.ballot_ids.add(generated_id)
                break
        return generated_id

def main():
    # load key
    Kc = RSA.importKey(open("public_client.pem", "r").read())
    Ks = RSA.importKey(open("public_server.pem", "r").read())
    Ks_inverse = RSA.importKey(open("prvkey_server.pem", "r").read())

    client_id_to_ballots_id = {}
    id_generator = ballot_id_generator()
    ballots_mapper = {}

    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    server_socket.bind((socket.gethostname(), 12345)) # cl3.learner.csie.ntu.edu.tw
    # become a server socket
    server_socket.listen(5)

    while True:
        # accept connections from outside
        client_socket, address = server_socket.accept()

        # ignore these lines
        # in this case, we'll pretend this is a threaded server
        # ct = client_thread(client_socket)
        # ct.run()

        print("Got connection from", address)
        client_socket_file = client_socket.makefile("rw")

        socket_send(client_socket_file, "Welcome to CNS 2016 i-voting system, please provide your id verification")

        # "client_id"
        client_id = socket_receive(client_socket_file)
        # id_1, id_2, id_3 = id_generator.generate_id(), id_generator.generate_id(), id_generator.generate_id()
        # ballots_mapper[client_id] = (id_1, id_2, id_3)
        ID1 = id_generator.generate_id()
        ballots_mapper[ID1] = (id_generator.generate_id(), id_generator.generate_id())
        ballots = "Hi {}! There are 3 candidates: 1.aaa 2.bbb 3.ccc".format(client_id)
        nonce = str(randrange(2<<80))
        # encrypted_message = create_encrypt(ballots+"||"+nonce, Kc)
        # signature = create_signature(encrypted_message, Ks_inverse)
        encrypted_message = Kc.encrypt(ballots+"||"+nonce, 32)
        signature = Ks_inverse.sign(encrypted_message, 32)

        socket_send(client_socket_file, encrypted_message)
        socket_send(client_socket_file, signature)

        # "(o,x,o);(x,x,o);(x,o,x)||nonce" encrypted by server's public key
        encrypted_message = socket_receive(client_socket_file)
        signature = socket_receive(client_socket_file)
        # check signature
        if not Kc.verify(encrypted_message, signature):
            print("wrong signature!!")
            # do something....

        # check if it's an useless ballot
        plaintext == Ks_inverse.decrypt(encrypted_message)
        vote_result = defaultdict(int)
        ballots = plaintext.split("|")[0].split(";")
        for ballot in ballots:
            ballot = ballot.strip("()").split(",")
            for vote_number in range(len(ballot)):
                if ballot[vote_number] == "o":
                    vote_result[vote_number+1] += 1
        number_1 = 0
        number_2 = 0
        for vote_number in range(len(ballot)):
            if vote_result[vote_number+1] == 1:
                number_1 += 1
            elif vote_result[vote_number+1] == 2:
                number_2 += 1
        if number_1+number_2 != len(ballot) or number_2 != 1:
            print("useless votes!!")
            with open("voting_result", "a") as voting_result_file:
                # ballot = (o,x,o)
                for ballot in ballots:
                    voting_result_file.write(ballot+" x\n")
        else:
            with open("voting_result", "a") as voting_result_file:
                # ballot = (o,x,o)
                for ballot in ballots:
                    voting_result_file.write(ballot+" o\n")

        # ID1 for client to check
        encrypted_message = Kc.encrypt(str(ID1), 32)
        signature = Ks_inverse.sign(encrypted_message, 32)
        socket_send(client_socket_file, encrypted_message)
        socket_send(client_socket_file, signature)

        # clent want to check
        encrypted_message = socket_receive(client_socket_file)
        signature = socket_receive(client_socket_file)
        # check signature
        if not Kc.verify(encrypted_message, signature):
            print("wrong signature!!")
            # do something....
        ID1 = int(Ks_inverse.decrypt(encrypted_message))
        # remain to be implemented


        # client_socket.send("Thank you for connecting")
        # client_socket.close()     
        client_socket_file.close()
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()

if __name__ == "__main__":
    main()