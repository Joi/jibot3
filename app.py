import glob
import importlib
import logging
import os
import re
import lib.slack as bolt
logging.basicConfig(
	level=logging.INFO,
	format='%(levelname)s:%(message)s'
)

def main():
	try:
		bolt.app()
	except KeyboardInterrupt:
		bolt.app.close()

if __name__ == "__main__":
	main()