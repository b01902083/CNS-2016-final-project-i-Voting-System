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
    Kc_inverse = RSA.importKey(open("prvkey_client.pem", "r").read())
	
	# create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
	server_socket.connect((socket.gethostname(), 12345)) # cl3.learner.csie.ntu.edu.tw
	
	server_socket_file = server_socket.makefile("rw")
	message=socket_receive(server_socket_file)
	print(message)
	
	socket_send(server_socket_file,ID)
	
	encrypted_message = socket_receive(server_socket_file)
    signature = socket_receive(server_socket_file)
	if not Ks.verify(encrypted_message, signature):
        print("wrong signature!!")
		# do something....
	
	#fill bollats
	print("vote rule: o for vote,x for against")
	plaintext == Kc_inverse.decrypt(encrypted_message)
	ballots = plaintext.split("|")[0].split(";")
	for ballot in ballots:
		print('ballot')
		for vote_number in range(len(ballot)):
			print('candidate')
			ballot[vote_number]=input()
	
	#give ballots to server
	nonce = str(randrange(2<<80))
	encrypted_message = Ks.encrypt(ballots+"||"+nonce, 32)
    signature = Kc_inverse.sign(encrypted_message, 32)
	socket_send(server_socket_file, encrypted_message)
    socket_send(server_socket_file, signature)
	
	#encrypted_message = Kc.encrypt(str(ID1), 32)
    #signature = Ks_inverse.sign(encrypted_message, 32)
    encrypted_message = socket_receive(server_socket_file)
    signature = socket_receive(server_socket_file)
	
	if not Ks.verify(encrypted_message, signature):
        print("wrong signature!!")
		# do something....
		
	bind_ID = int(Kc_inverse.decrypt(encrypted_message))
	print('ID for verify:')
	print(bind_ID);
	
	#verify
    socket_send(server_socket_file, encrypted_message)
    socket_send(server_socket_file, signature)
	
	encrypted_message = socket_receive(server_socket_file)
    signature = socket_receive(server_socket_file)
	plaintext=Kc_inverse.decrypt(encrypted_message)
	print('your vote:')
	print(plaintext)
	
	#disconnect
	server_socket_file.close()
    server_socket.shutdown(socket.SHUT_WR)
    server_socket.close()
	
if __name__ == "__main__":
    main()