import logging

def configureLogger(filename = 'log.txt', format = '%(asctime)s %(levelname)s: %(message)s', level = logging.DEBUG, date_format = '%d/%m/%Y %I:%M:%S %p'):
	logging.basicConfig(filename = 'log.txt', level = level, format = format, datefmt = date_format)
