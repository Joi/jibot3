# jibot3

A Slack Bot which currently only introduces itself and speaks nonsense when it sees the word "bot".

## Clone or download the source code

* **GitHub Repo:** [https://github.com/Joi/jibot3](https://github.com/Joi/jibot3)
* **GitHub CLI:** `gh repo clone Joi/jibot3`
* **HTTP:** `git clone https://github.com/Joi/jibot3.git`
* **SSH:** `git clone https://github.com/Joi/jibot3.git`

## Install Dependencies

1. `cd projectDirectory`
1. `npm install`

## Add Environment Variables

jibot3 requires Slack app tokens to communicate. The steps to retrieve this information is outlined in proceeding steps. These tokens are stored as environment variables. **Treat these tokens like passwords! Do not share them or check them into source code repos.**

1. `mkdir ./src/environments/`
1. Add and edit the following files:
	* `environments.ts`
		<pre><code>
		export const environment = {
			production: false,
			SLACK_CLIENT_ID: "[]",
			SLACK_APP_TOKEN: "[]",
			SLACK_BOT_TOKEN: "[]",
			SLACK_CLIENT_SECRET: "[]",
			SLACK_SIGNING_SECRET: "[]",
		};
		</code></pre>
	* `environments.prod.ts` (you only need this file if you will be deploying to a live environment)
		<pre><code>
		export const environment = {
			production: false,
			SLACK_CLIENT_ID: "[]",
			SLACK_APP_TOKEN: "[]",
			SLACK_BOT_TOKEN: "[]",
			SLACK_CLIENT_SECRET: "[]",
			SLACK_SIGNING_SECRET: "[]",
		};
		</code></pre>

## Build run and serve app
1. `npm run dev:ssr`
1. Open the live development server (usually located at [http://localhost:4200](http://localhost:4200)).
1. Ensure the app is installed in your slack workspace.  The steps to retrieve this information is outlined in proceeding steps.
1. Add your jibot to slack channels (Channel details -> More -> Add apps).
1. Interact with your jibot in channels to which the bot belongs or via direct message.

## Create & Configure a Slack APP

You can retrieve your create a Slack App or access your existing Slack apps at: [https://api.slack.com/apps](https://api.slack.com/apps). An overview of Slack app creation can be found at: [https://api.slack.com/start/overview#creating](https://api.slack.com/start/overview#creating). You may need to confer with a Slack Administrator to get this information.

1. ### Setup App-Level Token with scopes:
	* `connections:write`
	* `authorizations:read`
1. ### Enable Socket Mode
1. ### Set up OAuth scopes
	* `app_mentions:read`
	* `channels:history`
	* `channels:read`
	* `chat.write`
	* `im:history`
	* `users:read`
1. ### Subscribe to Bot Event Subscriptions
	* `app_mention`
	* `message.channels`
	* `message.im`
1. Install the app to your slack workspace. This is in the Basic Information area.
1. jibot can now be added to Slack channels or interacted with via direct message.