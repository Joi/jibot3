# Slack Messages
This directory contains plugins which are intended to respond to slack slack messages which contain a string or regular expression. 

## `keyword`
The keyword in these files should correspond to a triggering string or regular expression. Slack emoji's can be included as follows (or within a larger string or regular expression):

    keyword=":wave:"

## `callback_function`
The callback_function will be called when a triggering message is found. Currently two arguments are being passed into the message callback function, an message object containing context for the message request, and a say() function which allows the robot to respond with text in slack to the trigging message. It is likely that we will update this to pass all available arguments (**kwargs) and allow the developer to use as they see fit.