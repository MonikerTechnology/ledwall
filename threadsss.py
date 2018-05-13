import threading
import time
import sys
import os
import HTTPserver
import requests

run_one = True
run_two = True

print("Treasssss")
print("Treasssss")
print("Treasssss")
print("Treasssss")

# def one():
#     while run_one:
#         #print("one")
#         time.sleep(1)

# def two():
#     while run_two:
#         #print("two")
#         time.sleep(1)

# def startHTTPserver():
#     HTTPserver.start()
#     return()


# t1 = threading.Thread(target=one)
# t2 = threading.Thread(target=two)
# t3 = threading.Thread(target=startHTTPserver)

# t1.start()
# t2.start()
# t3.start()


# try:
#     while True:
#         print("is this working too?")
#         #print("number of threads: " + str(threading.activeCount()))
#         #time.sleep(5)
#         #print(t3.is_alive())
#         #time.sleep(1)
#         #message = HTTPserver.data
#         #print(message)
#         #print(message)
        
#         #HTTPserver.httpd.server_close()

# except KeyboardInterrupt:
#     HTTPserver.run = False
#     try:
#         r = requests.get("http://localhost:8080")
#     except:
#        pass
#     time.sleep(1)
#     print("Is the server thread running " + str(t3.is_alive()))
#     run_one = False
#     run_two = False
#     try:
#         sys.exit(0)
#     except SystemExit:
#         os._exit(0)


 