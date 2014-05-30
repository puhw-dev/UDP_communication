#!/usr/bin/python3
import socket
import struct
import logger
import logging
import utilities
import crypt

from custom_exc import AuthorizationException
from handler import MessageHandler


class Server:
	def __init__(self, UDP_IP = '127.0.0.1', UDP_PORT = 50009, BUFF = 16):
		self.__UDP_PORT = UDP_PORT
		self.__UDP_IP = UDP_IP
		self.__MAX_BUFF = BUFF
		self.__secret = 'passwOrd'
		self.__socket = None
		logger.configureLogger(file_name = '../logs/server_log_'+str(UDP_PORT)+'.txt')
		self.__db_path = '../monitor.db'
		self.__init_socket()
		self.__handle_connections()

	def __init_socket(self):
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.bind(('', self.__UDP_PORT))
		self.__socket.listen(5)

	def __handle_connections(self):
		while True:
			logging.debug('Waiting for connection')
			socket, address = self.__socket.accept()
			logging.debug('Accepting connection from {}:{}'.format(address[0], address[1]))
			message = self.__handler(socket, address)
			MessageHandler(self.__db_path, message, address[0]).start()

	def __handler(self, socket, address):
		message = b''
		try:
			self.__authorize(socket)		
			data_length = struct.unpack('L', socket.recv(8))[0]
			while data_length > 0: 
				chunk_size = min(data_length, self.__MAX_BUFF)
				message += socket.recv(chunk_size)
				data_length -= chunk_size
		except AuthorizationException as e:
			logging.exception(e)
		except IOError as e:
			logging.exception(e)
			message = b''	
		finally:
			socket.close()
			logging.debug('Connection with {}:{} closed'.format(self.__UDP_IP, self.__UDP_PORT))
		message = crypt.decrypt(message, self.__secret)
		logging.debug('Message received from {}:{} : {}'.format(self.__UDP_IP, self.__UDP_PORT, message))
		return message

	def __authorize(self, socket):
		sc = socket.recv(utilities.RAND_SIZE).decode('UTF-8').rstrip()
		cc = utilities.generate_random_value()
		cr = utilities.get_hashed_value(sc+cc+self.__secret)
		socket.send(bytes(cc, 'UTF-8'))
		socket.send(struct.pack('I', len(cr)))
		socket.send(bytes(cr, 'UTF-8'))
		sr_len = struct.unpack('I', socket.recv(4))[0]
		sr = socket.recv(sr_len).decode('UTF-8').rstrip()
		if cr != sr:
			raise AuthorizationException('Invalid credentials! No data will be accepted')
	
if __name__ == '__main__':
	server = Server()
