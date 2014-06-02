#!/usr/bin/python3
import socket
import sys
import struct
import logging
import json
import logger
import utilities
#import crypt

from Crypto.Cipher import AES
from custom_exc import AuthorizationException

class Client:
	def __init__(self, config_file):
		config = json.load(open(config_file))
		self.__UDP_PORT = config['server_port']
		self.__UDP_IP = config['server_ip']
		self.__secret = config['secret']
		self.__socket = None
		logger.configureLogger(file_name = '../logs/client_log_'+str(self.__UDP_PORT)+'.txt')

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
		sr = utilities.get_hashed_value(sc+cc+self.__secret)
		self.__socket.send(struct.pack('I', len(sr)))	
		self.__socket.send(bytes(sr, 'UTF-8'))
		
	def send_data(self, data):
		data = bytes(data, 'UTF-8')
		self.__init_socket()
		try:
			logging.debug('Communication started')
			self.__is_authorized()
			#data = crypt.encrypt(data, self.__secret)
			self.__socket.send(struct.pack('L', len(data)))
			self.__socket.send(data)
			logging.debug('Message sent')
		except AuthorizationException as e:
			self.__socket.send(struct.pack('L', 0))
			logging.exception(e)
		except IOError as e:
			logging.exception(e)
		finally:
			self.__socket.close()

if __name__ == '__main__':
	client = Client('../config/client_config.json')
	client.send_data("""{
	"message_type" : "register",
	"username" : "user1",
	"hostname" : "host2",
	"sensor_type" : "sys",
	"sensor_name" : "sensor2",
	"rpm" : 10
	}""")

	client.send_data("""{
	"message_type" : "measurement",
	"sensor_name" : "sensor2",
	"metrics_name" : "cpu",
	"data":
		{ "val":"65%", "time":"1/10/2014 11:11:10" }
	}""")

	client.send_data("""{
	"message_type" : "kil",
	"kill" : "sensor1"
	}""")
