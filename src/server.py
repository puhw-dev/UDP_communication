#!/usr/bin/python3
import socket
import struct
import logging
import json
import logger
import utilities
#import crypt

from custom_exc import AuthorizationException
from handler import MessageHandler


class Server:
	def __init__(self, config_file):
		config = json.load(open(config_file))
		self.__UDP_PORT = config['listen_on_port']
		self.__MAX_BUFF = config['buffer']
		self.__secret   = config['secret']
		self.__db_path  = config['db_path']
		self.__socket   = None
		logger.configureLogger(file_name = '../logs/server_log_'+str(self.__UDP_PORT)+'.txt')
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
		#message = b''
		message = ''
		try:
			self.__authorize(socket)		
			data_length = struct.unpack('L', socket.recv(8))[0]
			while data_length > 0: 
				chunk_size = min(data_length, self.__MAX_BUFF)
				message += socket.recv(chunk_size).decode('UTF-8')
				data_length -= chunk_size
		except AuthorizationException as e:
			logging.exception(e)
		except IOError as e:
			logging.exception(e)
			#message = b''	
			message = ''
		finally:
			socket.close()
			logging.debug('Connection with {}:{} closed'.format(address[0], address[1]))
		#message = crypt.decrypt(message, self.__secret)
		logging.debug('Message received from {}:{} : {}'.format(address[0], address[1], message))
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
	server = Server('../config/server_config.json')
