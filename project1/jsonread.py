import json
with open("input.json", "r") as f:
    data = json.load(f)

print(data["network"][0][1])
