import json


json_format_string = '{"answer": "Hello, User"}'
json_obj = json.loads(json_format_string)
key = "answer"

if key in json_obj:
    print(json_obj[key])
else:
    print(f"Key '{key}' is absent in JSON")