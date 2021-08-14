import json

with open('appearance_0814.json', 'r') as a:
    f1 = json.load(a)
    print(len(f1))

with open('appearance.json', 'r') as b:
    f2 = json.load(b)
    print(len(f2))

for i in range(10000):
    j1 = f1[i]
    j2 = f2[i]
    a, b = json.dumps(f1[i], sort_keys=True), json.dumps(f2[i], sort_keys=True)
    print(a == b)
    if a != b:
        print(a)
        print(b)

