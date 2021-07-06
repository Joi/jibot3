# Jibot Slack Plugins

Jibot plugins are a way to connect with slack events to provide interaction with users and/or processing the payload in some fasion.

Each of the .py files in this directory is loaded and checked for a keyword and classes which have names that correspond to a slack event type; for example when a user types a message containing "hello world" (`message` type with "hello world" keyword) or when a user visits the Jibot home tab (`event` type with keyword "app_home_opened"). If a keyword is not programatically specified, the filename (without the extension) will be used as the keyword.

## Event Types

### Message
Jibot can listen for messages which contain a string or regular expression in order to interact with users or process the payload in some way. Keyword may be a string or a regular expression.


### Event
Jibot can listen for specific events, for example `team_join` or `app_home_opened` in order to interact with users or process the payload in some way. Each event must be subscribed to within the [API UI](https://api.slack.com/apps/?).  Keyword is a string corresponding to a slack event for which a subscription has been created.

### Command
Jibot can listen for command (also called slash commands) events. Keyword is a string corresponding to a slash command which has been added in the [API UI](https://api.slack.com/apps/?). Commands must be acknolwedged with `ack()` to inform that the app received the event.

### Shortcut
A slack shortcut is a quick entry-point to Jibot from within slack, and can be configured to work globally (from within the text composer area) or within a message (via the context menu of an individual message). Shortcuts are similar to commands, but accept no direct user input. Keyword is a string or regular expression corresponding to a shortcut which has been added in the [API UI](https://api.slack.com/apps/?). Shortcuts must be acknolwedged with `ack()` to inform that the app received the event.

### Action
Jibot can listen to use actions, like button clicks and menu selections. Keyword is a string or regular expression corresponding to the unique identifiers of an interactive element. Actions must be acknolwedged with `ack()` to inform that the app received the event.

### View
Jibot can listen to the submitted values present within UI blocks. Keyword is a string or regular expression corresponding to the triggered action_id.

## Callback function args
The class  will be called when a triggering event is found. These functions are called with a set of arguments, each of which may be used (or not) and can be specified in any order. In addition to the arguments shown below, each event type contains a argument named to correspond to the event type (for example `action` and `message`) which is an alias of the payload object.

| Argument  | Description  |
| :---: | :--- |
| `body` | Dictionary that contains the entire body of the request (superset of `payload`). Some accessory data is only available outside of the payload (such as `trigger_id` and `authorizations`).
| `payload` | Contents of the incoming event. The payload structure depends on the listener. For example, for an Events API event, `payload` will be the [event type structure](https://api.slack.com/events-api#event_type_structure). For a block action, it will be the action from within the `actions` list. The `payload` dictionary is also accessible via the alias corresponding to the listener (`message`, `event`, `action`, `shortcut`, `view`, `command`, or `options`). For example, if you were building a `message()` listener, you could use the `payload` and `message` arguments interchangably. **An easy way to understand what's in a payload is to log it**. |
| `context` | Event context. This dictionary contains data about the event and app, such as the `botId`. Middleware can add additional context before the event is passed to listeners.
| `ack` | Function that **must** be called to acknowledge that your app received the incoming event. `ack` exists for all actions, shortcuts, view submissions, slash command and options requests. `ack` returns a promise that resolves when complete. Read more in [Acknowledging events](https://slack.dev/bolt-python/concepts#acknowledge).
| `respond` | Utility function that responds to incoming events **if** it contains a `response_url` (shortcuts, actions, and slash commands).
| `say` | Utility function to send a message to the channel associated with the incoming event. This argument is only available when the listener is triggered for events that contain a `channel_id` (the most common being `message` events). `say` accepts simple strings (for plain-text messages) and dictionaries (for messages containing blocks).
| `client` | Web API client that uses the token associated with the event. For single-workspace installations, the token is provided to the constructor. For multi-workspace installations, the token is returned by using [the OAuth library](https://slack.dev/bolt-python/concepts#authenticating-oauth), or manually using the `authorize` function.
| `logger` | The built-in [`logging.Logger`](https://docs.python.org/3/library/logging.html) instance you can use in middleware/listeners.