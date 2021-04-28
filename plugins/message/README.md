# Slack Messages
This directory contains plugins which are intended to respond to slack slack messages which contain a string or regular expression.

## Enable Events in your Slack App
Go to https://api.slack.com/apps/ and then, in the **Features** submenu, click **Event Subscriptions**

## Required Permissions
* message.channels

## `keyword`
The keyword in these files should correspond to a triggering string or regular expression. Slack emoji's can be included as follows (or within a larger string or regular expression):

    keyword=":wave:"

## `callback_function`
The callback_function will be called when a triggering message is found. These functions are called with a set of arguments, each of which can be used in any order. Please see the plugins directory README.md file for details about the callback function arguments.