import logging

def configureLogger(file_name = 'log.txt', format = '%(asctime)s %(levelname)s: %(message)s', level = logging.DEBUG, date_format = '%d/%m/%Y %I:%M:%S %p'):
	logging.basicConfig(filename = file_name, level = level, format = format, datefmt = date_format)
