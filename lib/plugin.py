from pathlib import Path
from types import ModuleType
class Plugin:
	file_name:str = None
	keyword:str = None
	type:str = None
	callback:callable = None
	def __init__(self, event_type, plugin_library:ModuleType):
		if hasattr(plugin_library, event_type):
			self.type = event_type
			self.callback = getattr(plugin_library, event_type)
			self.file_name = Path(plugin_library.__file__).stem
			if hasattr(self.callback, 'keyword'):
				self.keyword = getattr(self.callback, 'keyword')
			else: self.keyword = self.file_name