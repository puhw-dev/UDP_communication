#!/usr/bin/python3
import socket
import sys
import struct
import logger
import logging
import utilities
import crypt

from Crypto.Cipher import AES
from auth_exc import AuthorizationException

class Client:
	def __init__(self, UDP_IP = '127.0.0.1', UDP_PORT = 50009):
		self.__UDP_PORT = UDP_PORT
		self.__UDP_IP = UDP_IP
		self.__secret = 'passw0rd'
		self.__socket = None
		logger.configureLogger(file_name = '../logs/client_log_'+str(UDP_PORT)+'.txt')
		self.__init_socket()	

	def __init_socket(self):
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.connect((self.__UDP_IP, self.__UDP_PORT))
		
	def __is_authorized(self):
		sc = utilities.generate_random_value()
		self.__socket.send(bytes(sc, 'UTF-8'))
		cc = self.__socket.recv(utilities.RAND_SIZE).decode('UTF-8').rstrip()
		cr_len = struct.unpack('I', self.__socket.recv(4))[0]
		cr = self.__socket.recv(cr_len).decode('UTF-8').rstrip()
		sr = utilities.get_hashed_value(sc+cc+self.__secret)
		if cr != sr:
			raise AuthorizationException('Invalid credentials! No data will be sent.')
		
	def send_data(self, data):
		try:
			logging.debug('Communication started')
			self.__is_authorized()
			data = crypt.encrypt(data, self.__secret)
			self.__socket.send(struct.pack('L', len(data)))
			self.__socket.send(data)
			logging.debug('Success')
		except AuthorizationException as e:
			self.__socket.send(struct.pack('L', 0))
			logging.exception(e)
		except IOError as e:
			logging.exception(e)
		finally:
			self.__socket.close()

if __name__ == '__main__':
	client = Client()
	client.send_data(sys.argv[1])
