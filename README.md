# Jibot3 • A slack bot function compilerator
The intent of this code is to create a "garage" where you can park code to be used in a useful way within a chat bot interface (currently slack) without needing to know very much about the chat bot interface.

# Setup
The setup instructions presume that we have a slack robot setup already. The slack bot we have been using for the previous iteration of has permissions appropriate to this code. I will ammend these instructions with detailed information about slack bot setup and permissions once we determine where/how to move this code into existing jibot repo.

To install and run, you'll need python, and environment variables. I am using a .venv folder for a virtual environtment, and a .env file to hold & load environment variables, but how you accomplish this can vary based on your chosed OS, IDE, and shell evironment.

## Packages
	pip install slack-bolt

## Environment Variables
Replace [] values as shown below with the appropriate values from your slack bot configuration and import as appropriate to your local development environment.

	SLACK_SIGNING_SECRET=[...]
	SLACK_BOT_TOKEN=[xoxb-...]
	SLACK_APP_TOKEN=[xapp-...]

## Run the bot
	python ./app.py

## Adding plugins

The plugins directory is separated into folders which are currently based on the event types available in slack, and which likely have analogous event listeners in other chat bot integrations, should we eventually want to move to or add other bots / frameworks.

To add a plugin, simply add a new python file within the relevant event type directory in /plugins. The files in the plugins directories (currently each directory contains a `hello_world.py` to serve as an example) each contain two things,

1. 	`keyword`
1. 	`callback_function`

The intent of the **keyword** variable will depend from event to event. In a message event type, the keyword is a string or a regular expression which is used as a search expression to match messages in chat locations where the bot is. in a slash command, it would the a string like `'/hello_world'`

The **callback_function** will be run upon finding a matching event. The callback functions are currently only passed 2 arguments -- a payload object and a say function which allows for basic responses. This could probably be kwargs, but I think it's worthwhile to discuss your thoughts on this (not specifically about kwargs, but rather on whether we should expand the params passed to include more or all of them... I think keeping it simple until we need more is a reasonable approach)

## Notes:

### Slash Commands do not work
I am unsure of why the plugins/command/hello_world.py is not functional. I need to investigate that further. I was hoping that by making the functionality a step more generic that I would be sure I was handling the creation of listeners in a consistent way and the problem would become more apparent, but the symptoms have not changed (the slash commands do not appear within slack at all, there is no error generated). I have left the command folder in place because slash commands are pretty ubiquitious and expected bot functionality, the syntax should not need to change, and I'll be looking into why this isn't working next. It could likely pertain to timed ack() requirements...

**NOPE! It's slack bot permissions!** Time to see what we can do to minimize the need to continually update app permissions that is not simply blindly enabling everything up front (if possible). That should probably be the next step...
