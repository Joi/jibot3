# Slack Slash Commands
This directory contains plugins which are called as part of a slash command. This does not create a slash command, this sets up a listener for an existing slash command. You must first set up a slash command for your bot. In slack, the first word after the slash command will correspond to the filenames within this directory, for example, if your bot slash command is `/cozmobott` and a slack user types `/cozmobott hello_world` the callback_function within the `hello_world.py` will be executed (if it exists).

## To create a slash command:
1. Go to https://api.slack.com/apps/ and select the appropriate app
1. In the `**Features**` menu, click on `Slash Commands`
1. Click on the `Create New Command` button
1. Enter the command name and  short description
1. Optionally, enter a usage hint
1. Optionally, specify whether channels, users, and links are sent to the app unescaped

## `callback_function`
The callback_function will be called when a triggering command is found. These functions are called with a set of arguments, each of which can be used in any order. Please see the plugins directory README.md file for details about the callback function arguments.