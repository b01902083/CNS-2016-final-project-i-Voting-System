from Crypto.PublicKey import RSA
from Crypto import Random
from hashlib import sha256

def generateRSAKey():
	print "----- generating RSA key -----"
	random_generator = Random.new().read
	#generate pub and priv key
	key = RSA.generate(2048, random_generator)
	# print private key
	#print key.exportKey()

	# write into file
	f = open("./prvkey.pem", "w")
	f.write(key.exportKey())
	f.close()

	# print public key
	# print key.publickey().exportKey()
	# write into file
	f = open("./pubkey.pem", "w")
	f.write(key.publickey().exportKey())
	f.close()

	print "succefully generate RSA key and write into file"

def loadRSAKey():
	print "----- loading RSA key from file -----"
	pub = RSA.importKey(open("./pubkey.pem", "r").read())
	prv = RSA.importKey(open("./prvkey.pem", "r").read())
	return (pub, prv)

def testEncrypt(pub, prv):
	print "----- testing encryption -----"
	# encrypt and decrypt
	plaintext = "CNS{Proj5ctH1haha}"
	ciphertext = pub.encrypt(plaintext, 32)
	print "ciphertext = ", ciphertext
	if (plaintext == prv.decrypt(ciphertext)):
		print "Succefully decrypt, plaintext is ", plaintext
	else:
		print "Decrypt failed!"

def testSignature(pub, prv):
	print "----- testing signature -----"
	# signature and verify
	hashValue = sha256("CNS{Proj5ctH1haha}").digest()
	signature = prv.sign(hashValue, 32)
	print "signature is ", signature
	if (pub.verify(hashValue, signature)):
		print "signature is valid"
	else:
		print "signature is unvalid"


if __name__ == '__main__':
	generateRSAKey()
	pub, prv = loadRSAKey()

	testEncrypt(pub, prv)
	testSignature(pub, prv)
	