#!/usr/bin/python3
import sqlite3
import sys


class DBManager:
	def __init__(self, dbfile):
		self.__conn = sqlite3.connect(dbfile)

	def insert_into_sensor(self, values):
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO SENSOR (OWNER,HOSTNAME,HOSTIP,SENSORNAME,SENSORTYPE,RPM) VALUES (?,?,?,?,?,?)'
		cursor.execute(insert_stm, values)
		self.__conn.commit()
		cursor.close()
			
	def insert_into_metric(self, values):
		cursor = self.__conn.cursor()
		insert_stm = 'INSERT INTO METRIC (SENSORID,METRICNAME,TIME,VALUE) VALUES (?,?,?,?)'
		cursor.execute(insert_stm, values)
		self.__conn.commit()
		cursor.close()

	def get_sensor_id(self, sensor_name):
		cursor = self.__conn.cursor()
		select_stm = 'SELECT ID FROM SENSOR WHERE SENSORNAME==?'
		cursor.execute(select_stm, sensor_name)
		return cursor.fetchone()[0]
		
	
if __name__ == '__main__':
	manager = DBManager('../monitor.db')	
	sensor_val = ('a','b','c','sen3','e',2)
	#manager.insert_into_sensor(sensor_val)
	print(manager.get_sensor_id(('sen1',)))
	#manager.insert_into_metric(metric_val)
