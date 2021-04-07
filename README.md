# jibot3

A Slack Bot which:
1. introduces itself when @mentioned
1. responds with a rot13's when it sees a slack users say the word "bot"
1. watches channel messages which might pertain to books in it's database
1. has an sqlite3 database for data persistence
1. has an api backend which can generate word freqency distribution plots for text content within the database

## Recent New Stuff:
* New slack OAuth scope requirement:  `files.write`

## Clone or download the source code

* **GitHub Repo:** [https://github.com/Joi/jibot3](https://github.com/Joi/jibot3)
* **GitHub CLI:** `gh repo clone Joi/jibot3`
* **HTTP:** `git clone https://github.com/Joi/jibot3.git`
* **SSH:** `git clone git@github.com:Joi/jibot3.git`

## Install Dependencies
1. `cd projectDirectory`
1. `npm run install:all`

## EXCITING AND NEW! NLTK / Python / Oh My!
The python folder virtual envirment setup is not yet complete, and there are some steps to be done manually.
1. Installing python / pip (I am mac-based and use homebrew), see directions here: [https://docs.python-guide.org/starting/install3/osx/](https://docs.python-guide.org/starting/install3/osx/)
1. The npm "install:all" script will install ntlk but there is a downloader that must be run. first, cd to the python directory:
	* `cd src/python`
1. then, you can either:
	1. open an interactive python shell and run the following commands to open the downloader ui:
		* `import nltk`
		* `nltk.download()`
	1. or install every via command line by running:
		* `sudo python3 -m nltk.downloader -d /usr/local/share/nltk_data all`

## Add Environment Variables

jibot3 requires Slack app tokens to communicate. The steps to retrieve this information is outlined in proceeding steps. These tokens are stored as environment variables. **Treat these tokens like passwords! Do not share them or check them into source code repos.**

1. `mkdir ./src/environments/`
1. `touch ./src/environments/environments.ts`
1. Then add content to the files as shown, adding in your slack app tokens as appropriate:
	<pre><code>
		export const environment = {
			production: false,
			SLACK_CLIENT_ID: "",
			SLACK_APP_TOKEN: "",
			SLACK_BOT_TOKEN: "",
			SLACK_CLIENT_SECRET: "",
			SLACK_SIGNING_SECRET: "",
		};
	</code></pre>
1. If you will be deploying to a production environment, you will also need another file:
1. `touch ./src/environments/environments.prod.ts`
	<pre><code>
		export const environment = {
			production: false,
			SLACK_CLIENT_ID: "",
			SLACK_APP_TOKEN: "",
			SLACK_BOT_TOKEN: "",
			SLACK_CLIENT_SECRET: "",
			SLACK_SIGNING_SECRET: "",
		};
	</code></pre>

## Build run and serve database and app
1. `npm run start:db`
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
	* `files.write`
	* `im:history`
	* `users:read`
1. ### Subscribe to Bot Event Subscriptions
	* `app_mention`
	* `message.channels`
	* `message.im`
1. Install the app to your slack workspace. This is in the Basic Information area.
1. jibot can now be added to Slack channels or interacted with via direct message.