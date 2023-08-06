try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException


class BodyWrapper(object):
	def __init__(self):
		"""Creates an instance of BodyWrapper"""

		self.__users = None
		self.__key_modified = dict()

	def get_users(self):
		"""
		The method to get the users

		Returns:
			list: An instance of list
		"""

		return self.__users

	def set_users(self, users):
		"""
		The method to set the value to users

		Parameters:
			users (list) : An instance of list
		"""

		if not isinstance(users, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: users EXPECTED TYPE: list', None, None)
		
		self.__users = users
		self.__key_modified['users'] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string value

		Returns:
			int: A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if key in self.__key_modified:
			return self.__key_modified.get(key)
		
		return None

	def set_key_modified(self, key, modification):
		"""
		The method to mark the given key as modified

		Parameters:
			key (string) : A string value
			modification (int) : A int value
		"""

		if not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if not isinstance(modification, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modification EXPECTED TYPE: int', None, None)
		
		self.__key_modified[key] = modification
