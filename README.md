# Jibot3 • A slack bot
The intent of this code is to create a "garage" where you can park code to be used in a useful way within a chat bot interface (currently slack) without needing to know very much about the chat bot interface.

# **IMPORTANT NEW CHANGES!**:
**The environment variable names have changed!** Namespacing these variables allow us to store as much slack info we want in env vars, but to  select programatically which tokens to use when. Additionally, the bolt app loads any env vars which are present, which can cause error conditions, and this allows the app the sidestep that issue.

	JIBOT_SLACK_APP_TOKEN=[xapp-...]
	JIBOT_SLACK_BOT_TOKEN=[xoxb-...]
	...

# Slack Bot Creation
Here is a good introdocution and instructions for creating and configuring a slack bot: https://api.slack.com/bot-users.

## Recommended: Using [Socket Mode](https://app.slack.com/app-settings/T01LN1N5H60/A01LUFAPUFK/socket-mode)
Socket Mode is convenient, and is likely to work to serve jibot's needs for a while. Socket Mode allows for slack events to be "listened for" on your local computer without requiring a stable and internet-reachable dns name or IP address endpoint. Without socket mode, you'll need

## Slack Bot Oauth / Event Listening
The slack bot and web api client use of tokens and scopes. The tokens and scopes required will vary depending on your desired bot listeners and interactivity needs, however here is a basic guide to setting up tokens and scopes for use with jibot:

* If you plan to use socket mode, you must have an App-Level token with `connections:write` scope
	* https://api.slack.com/apps/ Settings -> Basic Information
* **Bot Token Scopes:** When an error is thrown, the missing scope will be specified in an error log. Start with the following, and add as you need: (https://api.slack.com/apps/ Settings -> OAuth & Permissions)
	* app_mentions:read (@bot_name_mentions)
	* channels:read (can get basic info about channel(s))
	* groups:read (can get basic info about private channel(s) to which the bot has been added)
	* im:read (can get basic info about direct message(s) to which the bot has been added)
	* team:read (can get basic info about the current team)
	* users:read (can get basic info about users(s))
	* chat:write (can write in channels/direct messages )
* **User Token Scopes** User token scopes allow access to api data and methods on behalf of the user which authorized/installed the slack application. At the moment, this has not been implemented, although if a user token is present and it is valid, it is used to establish the identity details of that user, for logging purposes.
* **Event Subscriptions:**
	* app_mention
	* message.channels
* **Incoming [Webhooks](https://api.slack.com/messaging/webhooks):**
WEBHOOKS ARE COMING! Please see the webhook readme files for details as they emerge.

# Project Setup
The setup instructions presume that we have a slack robot setup already. The slack bot we have been using for the previous iteration of has permissions appropriate to this code. I will ammend these instructions with detailed information about slack bot setup and permissions once we determine where/how to move this code into existing jibot repo.

## Packages
	pip install pyngrok
	pip install slack-bolt
	pip install slack_sdk

## Environment Variables
Replace [] values as shown below with the appropriate values from your slack bot configuration and import as appropriate to your local development environment. **BOT_TOKEN and SIGNING_SECRET are required. JIBOT_SLACK_APP_TOKEN is required to run in socket mode**

	JIBOT_SLACK_BOT_TOKEN=[xoxb-...]	# REQUIRED
	JIBOT_SLACK_SIGNING_SECRET=[...]	# REQUIRED
	JIBOT_SLACK_APP_TOKEN=[xapp-...]	# REQUIRED FOR SOCKET MODE

	JIBOT_DO_SOCKET_MODE=[True]		# Enable/disable Socket Mode	(default True)
	JIBOT_PORT=[3000]				# Port used for bot dev server	(default 3000)
	JIBOT_SLACK_SLASH_COMMAND=[...]	# Slash command for bot use
	JIBOT_SLACK_USER_TOKEN=[...]	# Currently Experimental
	JIBOT_SLACK_WEBHOOK_URL=[...]	# Webhook url

	JIBOT_NGROK_AUTH_TOKEN=[...]	# ngrok auth token for webhook proxy
	JIBOT_NGROK_HOSTNAME=[...]		# ngrok hostname

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

## Test the bot
If you have webhooks enabled and an evironment variable specified, the app will do some basic logging (in the channel specified when installing the webhook-enabled app). If you do not have webhooks enabled, you can test the bot as follows: in a channel which includes the bot, or in a direct message to the bot, send a message which include the phrase "hello world" (without quotes). The bot will reply with a message that includes the filename that is running the code.

## Adding plugins

The plugins directory is separated into folders which are currently based on the event types available in slack, and which likely have analogous event listeners in other chat bot integrations, should we eventually want to move to or add other bots / frameworks.

To add a plugin, simply add a new python file within the relevant event type directory in /plugins. In most cases, the filename is used to specify the "keyword" of the slack function involved, for example, the  `plugins/message/hello world.py` file is used to trigger an action when a slack message containing "hello world" is seen. The  `plugins/event/app_mention.py`, file is used to trigger an action when the bot is @mentioned.

The file must contain a function called `callback_function` which will be run upon finding a matching event. The arguments passed to the callback function are outlined in the [plugins folder README.md](https://github.com/Joi/jibot3/blob/main/plugins/README.md) and more information is available in each plugin subdirectory README.