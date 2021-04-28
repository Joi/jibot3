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
The callback_function will be called when a triggering command is found. These functions are called with a set of arguments, each of which can be used in any order. Please see the plugins directory README.md file for details about the callback function arguments.