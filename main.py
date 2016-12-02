import json
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
  username='{d9940f19-3ca0-4154-88dd-af102b9b701f}',
  password='{rcVDyr2CEIcg}',
  version='2016-09-20'
)

# Replace with the context obtained from the initial request
context = {}

workspace_id = '6846ffc4-07eb-45d9-a517-abe54e9f2dae'

response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': 'Hi'},
  context=context
)

print(json.dumps(response, indent=2))