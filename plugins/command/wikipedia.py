from include.wikipedia import callback_function
from lib.slack import slack_bot_slash_command as bot_slash_command
callback_function.__doc__ = f"Private Wikipedia lookup via slash command `/{bot_slash_command} wikipedia <search term or phrase>`"