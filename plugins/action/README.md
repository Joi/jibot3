# Actions
Actions are triggered by interactive components used inside views. A UI component, such as a button or text input, would be given an action_id, and the action_id corresponds to the name of the files within this directory.

## `callback_function`
The callback_function will be called when a triggering message is found. These functions are called with a set of arguments, each of which can be used in any order. Please see the plugins directory README.md file for details about the callback function arguments.