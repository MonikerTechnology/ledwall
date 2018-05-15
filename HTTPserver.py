#!/usr/bin/env python3

"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
import os
import colorsys
import log
file = str(os.path.basename(__file__))


power = 1
mode = "breathe"
H = 100
S = 100
V = 100
redMultiplier = 1.0
greenMultiplier = 1.0
blueMultiplier = 1.0
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
        log.info(file,"GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        

    def do_POST(self):
        global post_data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))
        #print

        message = post_data.decode('utf-8')
        message = json.loads(message)
        #message["state"]

        

        self._set_response()
        reply = {"state":"success"}
        reply["data"] = message
        reply = json.dumps(reply)
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(reply.encode('utf-8'))

def start(server_class=HTTPServer, handler_class=S, port=321):
    global httpd
    global postDic
    global power
    global mode
    global H
    global S
    global V
    global redMultiplier
    global greenMultiplier
    global blueMultiplier
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    time.sleep(.5)

    log.header(file,'Starting httpd...\n')

    while run:
        #log.info(file,"HTTPD still running")
        httpd.handle_request()
        #data = post_data.decode('utf-8')
        try:
            postDic = json.loads(post_data.decode('utf-8'))
            log.info(file,"See data: " + post_data.decode('utf-8'))
        except:
            log.warning(file,"Bad format, could not convert to JSON")
        try:
            if (postDic["type"] == "power"):
                power = postDic["power"] #int
                #log.header(file,"power set to: " + str(power))
            if (postDic["type"] == "mode"):
                mode = postDic["mode"].strip() #string
            if (postDic["type"] == "HSV"):
                H = postDic["HSV"]["H"]
                S = postDic["HSV"]["S"]
                V = postDic["HSV"]["V"]
                redMultiplier, greenMultiplier, blueMultiplier = colorsys.hsv_to_rgb(float(H), float(S), float(V))
                #print(str(redMultiplier) + " " + str(greenMultiplier))
        except:
            log.warning(file,"Bad format, does not begin with 'type' or failed to convert HSV")

        #httpd.serve_forever()
    httpd.server_close()
    log.info(file,'Stopping httpd...\n')

start()

# if __name__ == '__main__':
#     from sys import argv

#     if len(argv) == 2:
#         start(port=int(argv[1]))
#     else:
#         start()
#         #change this for port
