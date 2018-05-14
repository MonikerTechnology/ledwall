"""
This script gets dweets from dweet.io and forwards the "content" to the HTTPserver for the LED wall 
"""


import dweepy
import requests
import json
import os
import log
file = str(os.path.basename(__file__))



run = True #kill switch
def start():
    try:
        while run:
            try:
                for dweet in dweepy.listen_for_dweets_from('315novusledwall'):
                    
                    
                    log.info(file,dweet)
                    try:
                        dweet = json.dumps(dweet["content"])
                    except:
                        log.warning(file,"could not convert to JSON and extract contents")
                    try:
                        r = requests.post("http://localhost:321", data=dweet)
                    except:
                        log.warning(file,"Could not post to HTTPserver")
                    if (run == False):
                        log.warning(file,"breaking")
                        break

            except:
                log.warning(file,"Failed to get dweet")
    except KeyboardInterrupt:
        log.warning(file,'\ngoogleAssistant: Interrupt detected')
        #print("")
    
