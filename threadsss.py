import threading
import time
import sys
import os
import HTTPserver
import googleAssistant
import requests
#import main
try:
    import json
except ImportError:
    import simplejson as json

run_one = True
run_two = True

print("Treasssss")



def startHTTPserver():
    HTTPserver.start()
    return()

def startGoogleAssistant():
    googleAssistant.start()
    return()


t4 = threading.Thread(target=startHTTPserver)
t3 = threading.Thread(target=googleAssistant.start)

t3.start()
t4.start()


try:
    while True:
        #print("is this working too?")
        #print("number of threads: " + str(threading.activeCount()))
        #time.sleep(5)
        #print(t3.is_alive())
        time.sleep(4)
        print(HTTPserver.postDic["type"])
        #message = json.load(HTTPserver.data)
        try:
            message = json.load(HTTPserver.data)
            #mesage = message.json()
            print(message)
            print(HTTPserver.data)
        except:
            pass
        #HTTPserver.httpd.server_close()

except KeyboardInterrupt:
    HTTPserver.run = False
    try:
        r = requests.get("http://localhost:8080")
    except:
       pass
    time.sleep(1)
    print("Is the server thread running " + str(t3.is_alive()))
    run_one = False
    run_two = False
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


 