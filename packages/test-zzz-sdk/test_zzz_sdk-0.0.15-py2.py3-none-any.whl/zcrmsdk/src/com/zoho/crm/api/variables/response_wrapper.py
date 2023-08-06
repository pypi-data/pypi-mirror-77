try:
	from zcrmsdk.src.com.zoho.crm.api.util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.variables.response_handler import ResponseHandler
except Exception:
	from ..util import Constants
	from zcrmsdk.src.com.zoho.api.exception import SDKException
	from .response_handler import ResponseHandler


class ResponseWrapper(ResponseHandler):
	def __init__(self):
		"""Creates an instance of ResponseWrapper"""
		super().__init__()

		self.__variables = None
		self.__key_modified = dict()

	def get_variables(self):
		"""
		The method to get the variables

		Returns:
			list: An instance of list
		"""

		return self.__variables

	def set_variables(self, variables):
		"""
		The method to set the value to variables

		Parameters:
			variables (list) : An instance of list
		"""

		if not isinstance(variables, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: variables EXPECTED TYPE: list', None, None)
		
		self.__variables = variables
		self.__key_modified['variables'] = 1

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
