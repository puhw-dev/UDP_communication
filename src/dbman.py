#!/usr/bin/python3
import sqlite3
import sys


class DBManager:
	def __init__(self, dbfile):
		self.__conn = sqlite3.connect(dbfile)

	def insert_into_sensor(self, values):
		''' values - list of tuples '''
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO SENSOR VALUES (?,?,?,?,?)'
		for value in values:
			cursor.execute(insert_stm, value)
		self.__conn.commit()
		cursor.close()
			
	def insert_into_host(self, values):
		''' values - list of tuples '''
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO HOST VALUES (?,?,?)'
		for value in values:
			cursor.execute(insert_stm, value)
		self.__conn.commit()
		cursor.close()

	def insert_into_measurement(self, values):
		''' values - list of tuples '''
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO MEASUREMENT VALUES (?,?,?,?,?)'
		for value in values:
			cursor.execute(insert_stm, value)
		self.__conn.commit()
		cursor.close()

	def insert_into_metric(self, values):
		''' values - list of tuples '''
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO METRIC VALUES (?,?)'
		for value in values:
			cursor.execute(insert_stm, value)
		self.__conn.commit()
		cursor.close()

	
if __name__ == '__main__':
	manager = DBManager(sys.argv[1])	
	print(sys.argv[1])
	metric_val = [(1,'sys'),(2,'net'),(3,'sysl')]
	manager.insert_into_metric(metric_val)
