import ijson as ijson

f = open('drug-label-0001-of-0008.json')
objects = ijson.items(f, 'results.item')
for _object in objects:
    count = 0

print('done')