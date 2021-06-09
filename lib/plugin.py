import importlib
import re
class Plugin:
	event_name:str = None
	keyword:str = None
	regex:re = None
	type:str = None
	callback:callable = None
	def __init__(self, file_name:str, import_path:str, plugin_type:str):
		plugin_code = importlib.import_module(import_path)
		if hasattr(plugin_code, 'callback_function'):
			self.type = plugin_type
			self.callback = plugin_code.callback_function
			if hasattr(plugin_code, 'keyword'):
				if type(plugin_code.keyword) == type(re.compile("/.*/")):
					self.regex = plugin_code.keyword
					self.keyword = file_name
				else:
					self.keyword = plugin_code.keyword
			else:
				self.keyword = file_name
			arg_regex = re.compile("((?P<event_name>\w+)\/)?(?P<arg>\w+)")
			if type(self.keyword) == type(str()):
				matches = re.finditer(arg_regex, self.keyword)
				if matches is not None:
					for match in matches:
						event_name = match.group('event_name')
						if event_name is not None:
							self.event_name = event_name
							self.keyword = match.group('arg')