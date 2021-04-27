# Slack Slash Commands
This directory contains plugins which are intended to respond to slack slack slash command. This does not create a slash command, this sets up a listener for an existing slash command.

## To create a slash command:

1. Go to https://api.slack.com/apps/ and select the appropriate app
1. In the `**Features**` menu, click on `Slash Commands`
1. Click on the `Create New Command` button
1. Enter the command name and  short description
1. Optionally, enter a usage hint
1. Optionally, specify whether channels, users, and links are sent to the app unescaped

## `keyword`
The keyword in these files should correspond to the triggering slash command name.

## `callback_function`
The callback_function will be called when a triggering command is found. Currently two arguments are being passed into the command callback function, an command object containing context for the command request, and a say() function which allows the robot to respond with text in slack to the trigging command. It is likely that we will update this to pass all available arguments (**kwargs) and allow the developer to use as they see fit.