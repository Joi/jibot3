# Slack Events 
This directory contains plugins which are intended to respond to slack events. The use of the word "event" in this context is intended to specifically mean events which occur in slack (such as when a member joins the slack or leaves a channel), not the generic idea of event listeners. 

## `keyword`
The keyword in these files should correspond to the desired event name. 

**For a list and description of Slack API Events, visit <https://api.slack.com/events>**

***NOTE**: Be sure to check the "Works With" column. Only events that work with the Events API are available for use in this app.*

## `callback_function`
The callback_function will be called when a triggering event is found. Currently two arguments are being passed into the event callback function, an event object containing context for the event request, and a say() function which allows the robot to respond with text in slack to the trigging event. It is likely that we will update this to pass all available arguments (**kwargs) and allow the developer to use as they see fit.