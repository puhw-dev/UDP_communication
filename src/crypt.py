#!/usr/bin/python3
from Crypto.Cipher import AES
import hashlib
import base64

def encrypt(message, secret):
	cipher = AES.new(hashlib.sha256(bytes(secret, 'UTF-8')).digest())
	pad_msg = (message + (AES.block_size - len(message) % AES.block_size) * "\0")
	encrypted = base64.b64encode(cipher.encrypt(pad_msg))
	return encrypted
		
def decrypt(encrypted, secret):
	cipher = AES.new(hashlib.sha256(bytes(secret, 'UTF-8')).digest())
	decrypted = cipher.decrypt(base64.b64decode(encrypted)).decode('UTF-8')
	return decrypted.rstrip('\0')

if __name__ == '__main__':
	message = 'Test message with length not divisible by 16'
	print('Message {}, len {}'.format(message, len(message)))
	enc = encrypt(message, 'passw0rd')
	print('Encrypted {}, len {}'.format(enc, len(enc)))
	dec = decrypt(enc, 'passw0rd')
	print('Decrypted {}, len {}'.format(dec, len(dec)))
