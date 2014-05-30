#!/usr/bin/python3
import unittest
import subprocess
import sys


class SendRecieveTest(unittest.TestCase):
	def setUp(self):
		subprocess.call(['chmod','+x','run_module.sh', 'prep_db.sh', 'clear_logs.sh', 'check_db.sh', 'check_logs.sh'])
		subprocess.call('./prep_db.sh')
		subprocess.call('./clear_logs.sh')

	def test(self):
		subprocess.call('./run_module.sh')
		res = subprocess.check_output('./check_db.sh').decode().rstrip().split('\n')

		sensor_expected = '1|user1|host2|127.0.0.1|sensor2|sys|10'
		metric_expected = '1|1|cpu|1/10/2014 11:11:10|65%'

		self.assertTrue(res[0] == sensor_expected)
		self.assertTrue(res[1] == metric_expected)

		res = subprocess.check_output('./check_logs.sh').decode().rstrip().split('\n')

		self.assertTrue(res[0] == '3')
		self.assertTrue(res[1] == '3')
		self.assertTrue(res[2] == '3')
		self.assertTrue(res[3] == '2')


if __name__ == '__main__':
	pwd = subprocess.check_output('pwd').rstrip().decode()+"/../src/"
	sys.path.insert(0, pwd)
	from server import Server
	from client import Client
	unittest.main()
