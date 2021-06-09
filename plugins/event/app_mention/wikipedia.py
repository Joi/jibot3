import include.wikipedia as wikipedia

callback_function:callable =  wikipedia.callback_function
callback_function.__doc__ = f"Public Wikipedia lookup via bot `@mention wikipedia <search term or phrase>`"