import threading
import logging
import json

from dbman import DBManager
from custom_exc import UnknownMessageType


class MessageHandler(threading.Thread):
	def __init__(self, db_path, message, ip):
		super(MessageHandler, self).__init__()
		self.__db_path = db_path
		self.__sensor_ip = ip
		self.__message_type = None
		self.__message = message	
		self.__parse_message()

	def __parse_message(self):
		self.__data = json.loads(self.__message)
		self.__message_type = self.__data['message_type']

	def run(self):
		self.__db = DBManager(self.__db_path)
		if(self.__message_type == 'register'):
			self.__process_register_message()
		elif(self.__message_type == 'measurement'):
			self.__process_measurement_message()
		elif(self.__message_type == 'kill'):
			self.__process_kill_message()
		else:
			try:
				raise UnknownMessageType('Allowed message types are: register, measurement, kill')
			except UnknownMessageType as e:
				logging.exception('Message type {}'.format(self.__message_type))

	def __process_register_message(self):
		logging.debug('Processing register message')
		tuple_val = self.__data['username'], self.__data['hostname'], self.__sensor_ip, self.__data['sensor_name'], self.__data['sensor_type'], self.__data['rpm']
		self.__db.insert_into_sensor(tuple_val)	

	def __process_measurement_message(self):
		logging.debug('Processing measurement message')
		sensor_id = self.__db.get_sensor_id((self.__data['sensor_name'],))
		tuple_val = sensor_id, self.__data['metrics_name'], self.__data['data']['time'], self.__data['data']['val']
		self.__db.insert_into_metric(tuple_val)

	def __process_kill_message(self):	
		logging.debug('Processing kill message')
