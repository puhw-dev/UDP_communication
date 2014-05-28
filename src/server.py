#!/usr/bin/python3
import socket
import threading
import logger
import logging
import receiver

class Server:
	def __init__(self, UDP_IP = '127.0.0.1', UDP_PORT = 50009, BUFF = 16):
		self.__UDP_PORT = UDP_PORT
		self.__UDP_IP = UDP_IP
		self.__params = {}
		self.__params['MAX_BUFF'] = BUFF
		self.__params['secret'] = 'passw0rd'
		self.__socket = None
		logger.configureLogger()
		self.__init_socket()
		self.__handle_connections()

	def __init_socket(self):
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.bind(('', self.__UDP_PORT))
		self.__socket.listen(5)

	def __handle_connections(self):
		while True:
			logging.debug('Waiting for connection')
			self.__params['socket'], self.__params['address'] = self.__socket.accept()
			logging.debug('Accepting connection from {}:{}'.format(self.__params['address'][0], self.__params['address'][1]))
			receiver.MessageReceiver(self.__params).start()	
			#threading.Thread(target = self.__handler, args = (socket, address)).start()

if __name__ == '__main__':
	server = Server()
