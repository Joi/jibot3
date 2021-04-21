# Slack Slash Commands
This directory contains plugins which are intended to respond to slack slack slash command. 

## `keyword`
The keyword in these files should correspond to the triggering slash command. 

## `callback_function`
The callback_function will be called when a triggering command is found. Currently two arguments are being passed into the command callback function, an command object containing context for the command request, and a say() function which allows the robot to respond with text in slack to the trigging command. It is likely that we will update this to pass all available arguments (**kwargs) and allow the developer to use as they see fit.