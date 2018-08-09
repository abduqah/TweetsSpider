import json

j = []
with open('abdo.json') as f:
    d = f.read().rstrip().split('\n')
    while '' in d:
        d.remove('')
    for i in d:
        j.append(json.loads(i))

with open('ai-data', 'a') as f:
    for d in j:
        f.write(d.get('text') + '\n')