#!/usr/bin/env python3

"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
#import main

power = 0
mode = "startup"
H = 100
S = 100
V = 100
postDic = ""


try:
    import json
except ImportError:
    import simplejson as json

run = True

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        

    def do_POST(self):
        global post_data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        #print

        #message = post_data.decode('utf-8')
        #message = json.loads(message)
        #message["state"]

        

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def start(server_class=HTTPServer, handler_class=S, port=321):
    global httpd
    global postDic
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    time.sleep(.5)
    print
    print
    logging.info('Starting httpd...\n')

    while run:
        print("HTTPD still running")
        httpd.handle_request()
        #data = post_data.decode('utf-8')
        try:
            postDic = json.loads(post_data.decode('utf-8'))
            print(postDic)
            if (postDic["type"] == "power"):
                power = postDic["power"]
            if (postDic["type"] == "mode"):
                mode = postDic["mode"]
            if (postDic["type"] == "HSV"):
                H = postDic["HSV"]["H"]
                S = postDic["HSV"]["S"]
                V = postDic["HSV"]["V"]
        except:
            logging.info("Bad format, could not convert to JSON")
        #httpd.serve_forever()
    httpd.server_close()
    logging.info('Stopping httpd...\n')

#start()

# if __name__ == '__main__':
#     from sys import argv

#     if len(argv) == 2:
#         start(port=int(argv[1]))
#     else:
#         start()
#         #change this for port
