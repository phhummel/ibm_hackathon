import json
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
  username='{username}',
  password='{password}',
  version='2016-09-20'
)

# Replace with the context obtained from the initial request
context = {}

workspace_id = '25dfa8a0-0263-471b-8980-317e68c30488'

response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': 'Turn on the lights'},
  context=context
)

print(json.dumps(response, indent=2))