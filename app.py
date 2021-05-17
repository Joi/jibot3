
import lib.slack as bolt
import logging
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