class AuthorizationException(Exception):
	def __init__(self, info):
		self.__info = info

	def __str__(self):
		return repr(self.__info)
