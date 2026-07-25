import json
string = '{"name": "John", "age": 30}'
data = json.loads(string)
print(data['name'], data['age'])