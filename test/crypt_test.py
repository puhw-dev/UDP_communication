#!/usr/bin/python3
import unittest
import sys
import subprocess



class EncodingDecodingTest(unittest.TestCase):
	def test1(self):
		message = 'message1'
		secret = 'secret1'
		encrypted = encrypt(message, secret)
		decrypted = decrypt(encrypted, secret)
		self.assertTrue(message == decrypted)

	def test2(self):
		message = '1:<&6df(86};;<sdfh9+_)(*":]'
		secret = 'la3^*2)**&<;:'
		encrypted = encrypt(message, secret)
		decrypted = decrypt(encrypted, secret)
		self.assertTrue(message == decrypted)
	
	def test3(self):
		message = '{"message_type":"kill", "kill" : "sensor1"}'
		secret = 'passw0rd'
		encrypted = encrypt(message, secret)
		decrypted = decrypt(encrypted, secret)
		self.assertTrue(message == decrypted)


if __name__ == '__main__':
	pwd = subprocess.check_output('pwd').rstrip().decode()+"/../src/"
	sys.path.insert(0, pwd)
	from crypt import encrypt, decrypt
	unittest.main()
