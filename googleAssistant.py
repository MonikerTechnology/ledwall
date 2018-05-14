"""
This script gets dweets from dweet.io and forwards the "content" to the HTTPserver for the LED wall 
"""


import dweepy
import requests
import json



run = True #kill switch
def start():
    try:
        while run:
            try:
                for dweet in dweepy.listen_for_dweets_from('315novusledwall'):
                    
                    
                    print(dweet)
                    try:
                        dweet = json.dumps(dweet["content"])
                    except:
                        print("could not convert to JSON and extract contents")
                    #try:
                    r = requests.post("http://localhost:321", data=dweet)
                    #except:
                        #print("Could not post to HTTPserver")
                    if (run == False):
                        print("breaking")
                        break

            except:
                print("Failed to get dweet")
    except KeyboardInterrupt:
        print('\ngoogleAssistant: Interrupt detected')
        #print("")
    
