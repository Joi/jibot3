# Slack Events
This directory contains plugins which are intended to respond to slack events. The use of the word "event" in this context is intended to specifically mean events which occur in slack (such as when a member joins the slack or leaves a channel), not the generic idea of event listeners. The filename should correspond to a slack app event name.

## Enable Events in your Slack App
Go to https://api.slack.com/apps/ and then, in the **Features** submenu, click **Event Subscriptions**

## Required Permissions
* Your bot  must have permissions to the event you want to listen for, for example, if you want to listen for when the bot is @mentioned, you must subscribe to the `app_mention` event.

**For a list and description of Slack API Events, visit <https://api.slack.com/events>**

***NOTE**: Be sure to check the "Works With" column. Only events that work with the Events API are available for use in this app.*

### `callback_function`
The callback_function will be called when a triggering event is found. These functions are called with a set of arguments, each of which can be used in any order. Please see the plugins directory README.md file for details about the callback function arguments.