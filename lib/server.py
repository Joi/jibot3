from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import socket

class WebhookServerHandler(BaseHTTPRequestHandler):
	# def __init__(self, request:socket.socket, client_address, server:HTTPServer):
	# 	# dir_path = os.path.dirname(os.path.realpath(__file__))
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		logging.info(f"GET request, \nPath:{self.path} \nHeaders: \n{self.headers}\n")
		self._set_response()
		self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

	def do_POST(self):
		logging.info(f"POST request, \nPath:{self.path} \nHeaders: \n{self.headers}")
		# content_length = int(self.headers['Content-Length'])
		# post_data = self.rfile.read(content_length)
		self._set_response()
		self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))