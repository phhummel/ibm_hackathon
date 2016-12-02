import json
from os.path import join, dirname
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import TextToSpeechV1
import uuid

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
workspace_id = '6846ffc4-07eb-45d9-a517-abe54e9f2dae'

# generate filename for audio output
unique_filename = uuid.uuid4()

# Get response from trained answer model
response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': 'Hi'},
  context=context
)

# Unwrap answer
answer_cont = response['output']
answer_text = answer_cont['text']
answer = answer_text[0]

# store answer to .wav file
with open(join(dirname(__file__), 'resources/' + unique_filename.urn + '.wav'), 'wb+') as audio_file:
    audio_file.write(text_to_speech.synthesize(answer, accept='audio/wav', voice="en-US_AllisonVoice"))
