import json
string = '{"name": "John", "age": 30}'
data = json.loads(string)
print(json.dumps(data))