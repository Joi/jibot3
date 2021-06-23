from pathlib import Path
from types import ModuleType
class Plugin:
	event_types:list = [
		"action",
		"command",
		"event",
		"message",
		"shortcut"
	]
	event_name:str = None
	file_name:str = None
	keyword:str = None
	type:str = None
	callback:callable = None
	def __init__(self, plugin_library:ModuleType):
		for event_type in self.event_types:
			if hasattr(plugin_library, event_type):
				self.type = event_type
				self.callback = getattr(plugin_library, event_type)
				self.file_name = Path(plugin_library.__file__).stem
				if hasattr(self.callback, 'keyword'):
					self.keyword = getattr(self.callback, 'keyword')
				else: self.keyword = self.file_name