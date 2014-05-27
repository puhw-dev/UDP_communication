import hashlib
import string
import random
import os

RAND_SIZE = 50

def get_eth0_ip():
	return str(os.system("/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"))

def get_hashed_value(value):
	return hashlib.sha512(bytes(value, "UTF-8")).hexdigest()

def generate_random_value(size = RAND_SIZE, chars = string.ascii_uppercase + string.digits):
	return "".join(random.choice(chars) for _ in range(size))

if __name__ == "__main__":
	print(get_hashed_value("dupa"))

	print(generate_random_string())

	print(get_eth0_ip())
