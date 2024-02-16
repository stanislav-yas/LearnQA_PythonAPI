import json

json_string = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

json_obj = json.loads(json_string)
message2 = json_obj['messages'][1]['message']

print(message2) # "And this is a second message"