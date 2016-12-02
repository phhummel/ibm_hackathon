import json                                      # json 
import threading                                 # multi threading
import os                                        # for listing directories
import Queue                                     # queue used for thread syncronization
import sys                                       # system calls
import argparse                                  # for parsing arguments
import base64                                    # necessary to encode in base64 according to the RFC2045 standard 
import requests                                  # python HTTP requests library

# WebSockets 
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory, connectWS
from twisted.python import log
from twisted.internet import ssl, reactor

from sttClient import *


credentials = ['67d89d3e-94d7-4232-8c87-0b588f60cc49','ibvlcVN5HH3x']
model = 'en-US_BroadbandModel'
fileInput = './recordings.txt'
dirOutput = './output'
contentType = 'audio/wav'
threads = '1'
optOut = True 
tokenauth = True

# logging
log.startLogging(sys.stdout)

# add audio files to the processing queue
q = Queue.Queue()
lines = [line.rstrip('\n') for line in open( fileInput)]
fileNumber = 0
for fileName in(lines):
  q.put((fileNumber,fileName))   
  fileNumber += 1

hostname = "stream.watsonplatform.net"   
headers = {}
if ( optOut == True):      
  headers['X-WDC-PL-OPT-OUT'] = '1'

# authentication header
if  tokenauth:
  headers['X-Watson-Authorization-Token'] = Utils.getAuthenticationToken("https://" + hostname, 'speech-to-text', 
                                                                          credentials[0],  credentials[1])
else:
  string =  credentials[0] + ":" +  credentials[1]
  headers["Authorization"] = "Basic " + base64.b64encode(string)

# create a WS server factory with our protocol
url = "wss://" + hostname + "/speech-to-text/api/v1/recognize?model=" +  model
summary = {}
factory = WSInterfaceFactory(q, summary,  dirOutput,  contentType,  model, url, headers, debug=False)
factory.protocol = WSInterfaceProtocol

for i in range(min(int( threads),q.qsize())):

  factory.prepareUtterance()

  # SSL client context: default
  if factory.isSecure:
     contextFactory = ssl.ClientContextFactory()
  else:
     contextFactory = None
  connectWS(factory, contextFactory)

reactor.run()

# dump the hypotheses to the output file
fileHypotheses =  dirOutput + "/hypotheses.txt"
f = open(fileHypotheses,"w")
counter = 1
successful = 0 
emptyHypotheses = 0
for key, value in (sorted(summary.items())):
  if value['status']['code'] == 1000:
     #print key, ": ", value['status']['code'], " ", value['hypothesis'].encode('utf-8')
     successful += 1
     if value['hypothesis'][0] == "":
        emptyHypotheses += 1
  #else:
     #print str(key) + ": ", value['status']['code'], " REASON: ", value['status']['reason']
  f.write(str(counter) + ": " + value['hypothesis'].encode('utf-8') + "\n")
  counter += 1
f.close()

