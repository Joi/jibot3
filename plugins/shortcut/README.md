# Shortcuts
This directory contains plugins which are intended to respond to slack shortcuts. This does not create a shortcut, this sets up a listener for an existing slash shortcut.

## To create a shortcut:

1. Go to https://api.slack.com/apps/ and select the appropriate app
1. In the `**Features**` menu, click on `Interactivity & Shortcuts`
1. Click on the `Create New Shortcut` button
1. Chose between a global shortcut or a message-specific shortcut
1. Enter shortcut name, short description, and callback ID

## `keyword`
The keyword in these files should correspond to the triggering shortcuts callback ID.

## `callback_function`
The callback_function will be called when a triggering command is found. Currently two arguments are being passed into the command callback function, an command object containing context for the command request, and a say() function which allows the robot to respond with text in slack to the trigging command. It is likely that we will update this to pass all available arguments (**kwargs) and allow the developer to use as they see fit.