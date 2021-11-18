import json

with open('doro.json', encoding='utf-8') as f:
    data = json.load(f)

print(json.dumps(data, indent="\t", ensure_ascii = False))


icName = data['http://data.ex.co.kr:80/link/def/icName']['value']