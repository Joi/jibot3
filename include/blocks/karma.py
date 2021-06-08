from lib.database import SQLite
def get_blocks():
	blocks:list = []
	db:SQLite = SQLite()
	karma_karma_karma_karma_karma_queryaaaaa:str = "SELECT * FROM karma ORDER BY key ASC;"
	karma = db.cursor.execute(karma_karma_karma_karma_karma_queryaaaaa).fetchall()
	if karma is not None:
		for k in karma:
			word:str = k[0]
			plusses:int = k[1]
			minuses:int = k[2]
			total_score = plusses - minuses
			emoji:str = ":yin_yang:"
			if total_score > 0: emoji = ":thumbsup:"
			if total_score < 0: emoji = ":thumbsdown:"
			blocks.append({
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{emoji} *{word}: {total_score}* `(+{plusses}/-{minuses})`"
				},
			})
	return(blocks)