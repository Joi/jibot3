# [Slack Webhooks](https://api.slack.com/messaging/webhooks)

## **IMPORTANT NOTE**
**This is at the begining stages of implementation. Instructions which are included are the beginings of outlining the how-to part, but it does not currently achieve demonstrable (within slack) results!**

If webhooks are enabled, a webhook URL is created upon the installation of an app and the installation process will ask which slack channel the webhook should send its output to.  Webhooks are a super-convenient way to send message into your slack which are triggered from external services, however external service webhooks may be in an improper format,  unable to be directly handled by the slack webhook url.

We're building a way to use ngrok and a simple http server to act as a webhook proxy, so you can recieve http requests with data, do stuff with the data, and pass the properly formatted data to the slack webhook url so the message is sent and displayed in slack.

## Enable webhooks
* Go to the [slack api dashboard](https://api.slack.com/apps/), select your app, then in the **Features** menu, click **Incoming Webhooks** and set the switch to **on**.
* Create a new webhook URL, there are no options to provide.
* Copy the webhook URL and set the environment variable (`JIBOT_SLACK_WEBHOOK_URL`) as described in the [main README.md](https://github.com/Joi/jibot3/blob/main/README.md)

## [`ngrok`](https://ngrok.com/) & [`pyngrok`](https://pypi.org/project/pyngrok/)
ngrok/pngrok aren't web servers, they are tunnels to connect a local web server to an internet reachable address. By combining ngrok and a python simple http server, we are creating a simple webserver to act as a python proxy, and using ngrok/pyngrok makes this webserver accessible to the wider world.

## **MORE DETAILS AND HOW-TO COMING SOON**

<!--
## A Quick Solution: Response URL using [`ngrok`](https://ngrok.com/) & [`pyngrok`](https://pypi.org/project/pyngrok/)
 Code to support ngrok and pyngrok are in place to facilitate creating a live request URL, and will be used in place of socket mode to act as a fully functioning live request url.  If an environment variable called `NGROK_AUTH_TOKEN` is present, it will be used to establish a live http tunnel to be used as your apps Request Url. If you have a ngrok subdomain or custom domain, you can specify that via an environment variable called `NGROK_HOSTNAME.`

 To configure the request url, go to https://api.slack.com/apps, select the appropriate app, then:
 1. In the **Settings** menu, click on **Socket Mode**, then disable socket mode
 1. In the **Features** Menu, click on **Event Subscriptions**, ensure events is enabled, then
 1. Enter the Request Url, followed by /slack/events, for example:
 	* my ngrok url is: `http://cozmobott.ngrok.io`
	* My slack request url is: `http://cozmobott.ngrok.io/slack/events` -->
