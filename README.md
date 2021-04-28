# Jibot3 • A slack bot
The intent of this code is to create a "garage" where you can park code to be used in a useful way within a chat bot interface (currently slack) without needing to know very much about the chat bot interface.

# New Notes:

## [Socket Mode](https://app.slack.com/app-settings/T01LN1N5H60/A01LUFAPUFK/socket-mode) Considerations

Socket Mode is convenient, but it restricts the capabilities pretty drastically, most notably as it relates to incoming webhooks from external services. A reproducible development environment which allows for a real request url is an important step in allowing external triggers and data to come into slack. There are various ways to create a live url to host this code, including: [regular-old-hosting](https://api.slack.com/docs/hosting), dynamic DNS services, and tunneling, each with pros and cons and ease of use considerations.

### A Quick Solution: Response URL using [`ngrok`](https://ngrok.com/) & [`pyngrok`](https://pypi.org/project/pyngrok/)
 Code to support ngrok and pyngrok are in place to facilitate creating a live request URL, and will be used in place of socket mode to act as a fully functioning live request url.  If an environment variable called `NGROK_AUTH_TOKEN` is present, it will be used to establish a live http tunnel to be used as your apps Request Url. If you have a ngrok subdomain or custom domain, you can specify that via an environment variable called `NGROK_HOSTNAME.`

 To configure the request url, go to https://api.slack.com/apps, select the appropriate app, then:
 1. In the **Settings** menu, click on **Socket Mode**, then disable socket mode
 1. In the **Features** Menu, click on **Event Subscriptions**, ensure events is endabled, then
 1. Enter the Request Url, followed by /slack/events, for example:
 	* my ngrok url is: `http://cozmobott.ngrok.io`
	* My slack request url is: `http://cozmobott.ngrok.io/slack/events`

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
	NGROK_AUTH_TOKEN=[OPTIONAL:your-ngrok-auth-token]

## Run the bot
	python ./app.py

## Adding plugins

The plugins directory is separated into folders which are currently based on the event types available in slack, and which likely have analogous event listeners in other chat bot integrations, should we eventually want to move to or add other bots / frameworks.

To add a plugin, simply add a new python file within the relevant event type directory in /plugins. The files in the plugins directories (currently each directory contains a `hello_world.py` to serve as an example) each contain two things,

1. 	`keyword`
1. 	`callback_function`

The intent of the **keyword** variable will depend from event to event. In a message event type, the keyword is a string or a regular expression which is used as a search expression to match messages in chat locations where the bot is. in a slash command, it would the a string like `'/hello_world'`

The **callback_function** will be run upon finding a matching event. The callback functions are currently only passed 2 arguments -- a payload object and a say function which allows for basic responses. This could probably be kwargs, but I think it's worthwhile to discuss your thoughts on this (not specifically about kwargs, but rather on whether we should expand the params passed to include more or all of them... I think keeping it simple until we need more is a reasonable approach)
