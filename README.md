# Jibot3 • A slack bot
The intent of this code is to create a "garage" where you can park code to be used in a useful way within a chat bot interface (currently slack) without needing to know very much about the chat bot interface.

# **IMPORTANT NEW CHANGES!**:
**The environment variable names have changed!** Namespacing these variables allow us to store as much slack info we want in env vars, but to  select programatically which tokens to use when. Additionally, the bolt app loads any env vars which are present, which can cause error conditions, and this allows the app the sidestep that issue.

	JIBOT_SLACK_APP_TOKEN=[xapp-...]
	JIBOT_SLACK_BOT_TOKEN=[xoxb-...]
	...

# Slack Bot Creation
Here is a good introduction and instructions for creating and configuring a slack bot: [Slack Bot User Overview](https://api.slack.com/bot-users).

## Recommended: Using [Socket Mode](https://app.slack.com/app-settings/T01LN1N5H60/A01LUFAPUFK/socket-mode)
Socket Mode is convenient, and is likely to work to serve jibot's needs for a while. Socket Mode allows for slack events to be "listened for" on your local computer without requiring a stable and internet-reachable dns name or IP address endpoint. Without socket mode, you'll need

## Recommended Shortcuts
The bot is created to work with a slack shortcut with a callback ID called `jibot`, but you have to create that within the slack api configuration, here is a basic guide to set up a shortcut:
* https://api.slack.com/apps/ Features -> Interactivity & Shortcuts
	* Click on the Create New Shortcut button
	* Name: This may be anything you prefer, and is the name shown in the shortcut menu
	* Short Description: This May be anything you prefer, and may not be visible in the shortcut menu
	* Callback ID: **REQUIRED** must be set to `jibot`

## Slack Bot Oauth / Event Listening
The slack bot and web api client use of tokens and scopes. The tokens and scopes required will vary depending on your desired bot listeners and interactivity needs, however here is a basic guide to setting up tokens and scopes for use with jibot:

* To use Socket Mode, you must have an App-Level token with `connections:write` scope
	* [Settings -> Basic Information](https://api.slack.com/apps/)

* **Bot Token Scopes:** When an error is thrown, the missing scope will be specified in an error log. Start with the following, and add as you need: [Settings -> OAuth & Permissions](https://api.slack.com/apps/)
	* [app_mentions:read](https://api.slack.com/scopes/app_mentions:read)
	* [channels:read](https://api.slack.com/scopes/channels:read)
	* [groups:read](https://api.slack.com/scopes/groups:read)
	* [im:read](https://api.slack.com/scopes/im:read)
	* [team:read](https://api.slack.com/scopes/team:read)
	* [users:read](https://api.slack.com/scopes/users:read)
	* [chat:write](https://api.slack.com/scopes/chat:write)

* **User Token Scopes** User token scopes allow access to api data and methods on behalf of the user which authorized/installed the slack application.
	* [identity.basic](https://api.slack.com/scopes/identity.basic)

* **Event Subscriptions:**
	* [app_home_opened](https://api.slack.com/events/app_home_opened)
	* [app_mention](https://api.slack.com/events/app_mention)
	* [message.channels](https://api.slack.com/events/message.channels)

# Project Setup

## Packages
	pip install slack-bolt
	pip install slack_sdk
	pip install stop_words
	pip install wikipedia
	pip install Pyzotero
	pip install cryptography

## Environment Variables
Replace [] values as shown below with the appropriate values from your slack bot configuration and import as appropriate to your local development environment. **BOT_TOKEN and SIGNING_SECRET are required. JIBOT_SLACK_APP_TOKEN is required to run in socket mode**

	JIBOT_SLACK_BOT_TOKEN=[xoxb-...]	# REQUIRED
	JIBOT_SLACK_SIGNING_SECRET=[...]	# REQUIRED
	JIBOT_SLACK_APP_TOKEN=[xapp-...]	# REQUIRED FOR SOCKET MODE
	JIBOT_PORT=[3000]					# Port used for bot dev server	(default 3000)
	JIBOT_SLACK_SLASH_COMMAND=[...]		# Slash command for bot use
	JIBOT_SLACK_USER_TOKEN=[...]		# Currently Experimental
	JIBOT_CRYPTO_PASS_PHRASE=[PASSPHRASE]	# Used to create key to encrypt/decript sensitive stuff in db

### Using virtual environment and adding your environment variables
I (pegnott) am using VS Code on  MacOS...  I set up a virtual environment, and adding environment variables to be loaded on activations. Here's how I did it:
* Install the [Microsoft Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* `python -m venv [venv_directory]`
* `touch [venv_directory]/.env`
* edit venv.env file to include the variables as shown above.
* update venv/bin/activate.  Around line 40, there is a line that looks like:

		export VIRTUAL_ENV

* Add the following below it:

		set -a
		source $VIRTUAL_ENV/.env
		set +a

* Activate the virtual environment:

		source ./[venv_directory]/bin/activate

* NOTE: The MS Python extension for VS Code will ask if you want to use this as a workspace -- doing so will mean that when you open a new terminal window, the virtual environment will be acticvated automatically, allowing you to skip this step next time.

## Run the bot
	python ./app.py
	The bot should say hello & goodbye on startup and shutdown

## Adding plugins

The plugins directory is separated into folders which are currently based on the event types available in slack, and which likely have analogous event listeners in other chat bot integrations, should we eventually want to move to or add other bots / frameworks.

To add a plugin, simply add a new python file within the relevant event type directory in /plugins. In most cases, the filename is used to specify the "keyword" of the slack function involved, for example, the  `plugins/message/hello world.py` file is used to trigger an action when a slack message containing "hello world" is seen. The `plugins/event/app_home_opened.py`, file is used to trigger an action when a user navigates to the bot home tab.

There can be envisioned cases where one would want to reuse named events, and modify the response based on other contextual information. To facilitate this, we allow for a file structure as follows:
`plugins/event/event_name/keyword.py`

So for example, the `plugins/event/app_mention/wikipedia.py` is triggred by `@bot_name wikipedia [SEARCH WORD OR PHRASE]`

The file must contain a function called `callback_function` which will be run upon finding a matching event. The arguments passed to the callback function are outlined in the [plugins folder README.md](https://github.com/Joi/jibot3/blob/main/plugins/README.md) and more information is available in each plugin subdirectory README.
