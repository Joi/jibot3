import glob
import importlib
import logging
import os
import re
import lib.slack

logging.basicConfig(level=logging.ERROR)
plugins = []

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
		"path": matches.group(0).replace(".py", "").replace("/","."),
		"type": matches.group(1),
		"name": matches.group(2),
	}
	info['lib'] = importlib.import_module(info.get('path'))
	return info

def init_slack():
	global plugins
	print("Initializing slack...")
	slack = lib.slack.app(
		app_token=os.environ["SLACK_APP_TOKEN"],
		signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
		token=os.environ.get("SLACK_BOT_TOKEN"),
	)
	print("Loading slack plugins...")
	for plugin in plugins:
		plugin_name = plugin.get('name')
		event_type = plugin.get('type')
		keyword = plugin.get('lib').keyword
		callback_function = plugin.get('lib').callback_function
		slack(event_type,  keyword, callback_function)
		print(event_type + ": " + plugin_name + "...")
	slack.socket_mode.start()

def main():
	init_plugins()
	init_slack()

if __name__ == "__main__":
	main()