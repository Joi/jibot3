# jibot3
A Slack Bot

## Create & Configure a Slack APP
You can retrieve your create a Slack App or access your existing Slack apps at: https://api.slack.com/apps
An overview of Slack app creation can be found at: https://api.slack.com/start/overview#creating.

1. ### Setup App-Level Token with scopes:
	1. connections:write
	1. authorizations:read
1. ### Enable Socket Mode
1. ### Set up OAuth scopes
	1. app_mentions:read
	1. channels.history
	1. channels:read
	1. chat.write
	1. im:history
	1. users:read
1. ### Subscribe to Bot Event Subscriptions
	1. app_mention
	1. message.channels
	1. message.im

## Add Environment Variables
You can retrieve your create a Slack API or retrieve your existing Slack APP API tokens from: https://api.slack.com/apps.
1. SLACK_APP_TOKEN
1. SLACK_BOT_TOKEN
1. SLACK_SIGNING_SECRET
