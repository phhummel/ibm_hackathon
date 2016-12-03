import json
from os.path import join, dirname
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import TextToSpeechV1
import uuid

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

# speech-to-text object credentials
credentials = ['67d89d3e-94d7-4232-8c87-0b588f60cc49','ibvlcVN5HH3x']
model = 'en-US_BroadbandModel'
fileInput = './recordings.txt'
dirOutput = './output'
contentType = 'audio/wav'
threads = '1'
optOut = True 
tokenauth = True

# New conversation object - add to the library on 
# https://www.ibmwatsonconversation.com
conversation = ConversationV1(
  username='d9940f19-3ca0-4154-88dd-af102b9b701f',
  password='rcVDyr2CEIcg',
  version='2016-09-20'
)
# Text to speech module
text_to_speech = TextToSpeechV1(
    username='28a1b1ed-4207-4397-96f8-13970d0778dd',
    password='O8aPGSZ0ALGZ',
    x_watson_learning_opt_out=True)  # Optional flag

# Replace with the context obtained from the initial request
context = {}

# Create a new workspace for useful conversations
#Simple Hello World
#workspace_id = '6846ffc4-07eb-45d9-a517-abe54e9f2dae'
workspace_id = 'ce471236-b537-4225-b95e-5b1b5861e3d2'
# generate filename for audio output
unique_filename = uuid.uuid4()


# add audio files to the processing queue
q = Queue.Queue()
lines = [line.rstrip('\n') for line in open( fileInput)]
fileNumber = 0
for fileName in(lines):
  q.put((fileNumber,fileName))   
  fileNumber += 1
  print fileName

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

for key, value in (sorted(summary.items())):
	hypo = value['hypothesis'].encode('utf-8')


# Get response from trained answer model
temp = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': '  '},
  context=context
)
response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': hypo},
  context=temp['context']
)

# Unwrap answer
answer_cont = response['output']
answer_text = answer_cont['text']
answer = answer_text[0]

# store answer to .wav file
with open(join(dirname(__file__), 'resources/' + unique_filename.urn + '.wav'), 'wb+') as audio_file:
    audio_file.write(text_to_speech.synthesize(answer, accept='audio/wav', voice="en-US_AllisonVoice"))
