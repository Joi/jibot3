import logging
import os
import lib.slack as bolt

logging.basicConfig(
	level=logging.INFO,
	format='%(levelname)s:%(message)s'
)
def init_db():
	db_file = f"{os.getcwd()}{os.sep}sqlite.db"
	if os.path.exists(db_file):
		logging.debug(f"Database file exists... {db_file}")
	else:
		logging.debug(f"Database file does not exist... creating {db_file}")
		try:
			os.mknod(db_file)
		except:
			with open(db_file, 'w'): pass

def main():
	init_db()
	bolt.app()

if __name__ == "__main__":
	main()