import lib.slack as bolt
import logging

logging.basicConfig(
	level=logging.INFO,
	format='%(levelname)s:%(message)s'
)
bolt.app()