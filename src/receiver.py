import threading
import socket
import struct
import logger
import logging
import utilities
import crypt


class MessageReceiver(threading.Thread):
	def __init__(self, params):
		threading.Thread.__init__(self)
		self.__params = params
		self.__UDP_PORT = params['address'][1]
		self.__UDP_IP = params['address'][0]
		self.__MAX_BUFF = params['MAX_BUFF']
		self.__socket = params['socket']
		self.__secret = params['secret']
		self.__message = None

	def run(self):
		message = b''
		try:
			self.__authorize(self.__socket)		
			data_length = struct.unpack('L', self.__socket.recv(8))[0]
			while data_length > 0: 
				chunk_size = min(data_length, self.__MAX_BUFF)
				message += self.__socket.recv(chunk_size)
				data_length -= chunk_size
		except IOError as e:
			logging.exception(e)
			message = b''	
		finally:
			self.__socket.close()
			logging.debug('Connection with {}:{} closed'.format(self.__UDP_IP, self.__UDP_PORT))
		self.__message = crypt.decrypt(message, self.__secret)
		logging.debug('Message received from {}:{} : {}'.format(self.__UDP_IP, self.__UDP_PORT, self.__message))

	def __authorize(self, socket):
		sc = socket.recv(utilities.RAND_SIZE).decode('UTF-8').rstrip()
		cc = utilities.generate_random_value()
		cr = utilities.get_hashed_value(sc+cc+self.__params['secret'])
		socket.send(bytes(cc, 'UTF-8'))
		socket.send(struct.pack('I', len(cr)))
		socket.send(bytes(cr, 'UTF-8'))
		

if __name__ == '__main__':
	print('Nothing to see here...')
