try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.currencies.action_handler import ActionHandler
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .action_handler import ActionHandler


class ActionWrapper(ActionHandler):
	def __init__(self):
		"""Creates an instance of ActionWrapper"""

		self.__currencies = None
		self.__key_modified = dict()

	def get_currencies(self):
		"""
		The method to get the currencies

		Returns:
			list: An instance of list
		"""

		return self.__currencies

	def set_currencies(self, currencies):
		"""
		The method to set the value to currencies

		Parameters:
			currencies (list) : An instance of list
		"""

		if not isinstance(currencies, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: currencies EXPECTED TYPE: list', None, None)
		
		self.__currencies = currencies
		self.__key_modified['currencies'] = 1

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
