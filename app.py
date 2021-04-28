import glob
import importlib
import logging
import os
import re
import lib.slack as bolt

logging.basicConfig(level=logging.ERROR)
plugins = []
slack = None
def init_plugins():
	global plugins
	app_dir = os.path.dirname(os.path.realpath(__file__))
	plugins_dir = app_dir + os.sep +  'plugins'
	plugin_files = glob.glob(plugins_dir + os.sep + "**" + os.sep + "[!__]*.py", recursive=True)
	for plugin_path in plugin_files:
		relative_path = os.path.relpath(plugin_path, os.getcwd())
		plugins.append(plugin_info_from_path(relative_path))

def plugin_info_from_path(plugin_path):
	path_regex = re.compile("^plugins\/(\w+)\/(.+)\.py$")
	matches = path_regex.match(plugin_path)
	info = {
		"path": plugin_path,
		"import_path": matches.group(0).replace(".py", "").replace("/","."),
		"type": matches.group(1),
		"name": matches.group(2),
	}
	info['lib'] = importlib.import_module(info.get('import_path'))
	return info

def init_slack():
	global plugins
	global slack
	print("Initializing slack...")
	slack = bolt.app()
	print("Loading slack plugins...")
	for plugin in plugins:
		plugin_name = plugin.get('name')
		event_type = plugin.get('type')
		keyword = plugin.get('lib').keyword
		callback_function = plugin.get('lib').callback_function
		slack.event_listener(event_type,  keyword, callback_function)
		print('\t' + plugin.get('path') + " (" + keyword + ")")
	slack.start()

def main():
	global slack
	try:
		init_plugins()
		init_slack()
	except KeyboardInterrupt:
		print("App closed with keyboard interrupt... Shutting down...")
		slack.close()

if __name__ == "__main__":
	main()