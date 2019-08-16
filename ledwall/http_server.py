#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""

# curl -X GET 'http://localhost:8080/?id=3&hsv=1,2,3&mode=pizza'
# curl -X GET 'http://localhost:8080/?id=3&power=1&mode=audio_bars'

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import urllib.parse as urlparse
from ledwall.settings import Settings

httpd = None
server_thread = None


class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)  # This causes local log line
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        self._set_response()

        # This goes to client
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        # get the parameters
        parsed = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed.query)

        Settings.update_values(**params)

    def do_POST(self):
        # TODO: confugure post to update http_data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def start_server():
    global server_thread
    server_thread = threading.Thread(target=_run, args=())
    server_thread.start()


def _run(server_class=HTTPServer, handler_class=S, port=8080):
    global httpd
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
        print('server closed')
        # httpd.handle_request()
        # print('handled request')
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        # run(port=int(argv[1]))
        start_server()

    else:
        # run()
        start_server()
