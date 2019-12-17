import json

inv = {}
loc = {}
with open('docs/json/inventory.json') as f:

    inventory = json.load(f)

for item in inventory['Inventories']:
    if item['ItemNumber'] not in inv.keys():
        inv[item['ItemNumber']] = []
    inv[item['ItemNumber']].append({item['Location']: item['Quantity']})

for item in inventory['Inventories']:
    if item['Location'] not in loc.keys():
        loc[item['Location']] = {}
    loc[item['Location']][item['ItemNumber']] = item['Quantity']

with open('docs/json/sku_inv.json', 'w') as outfile:
    json.dump(inv, outfile)

with open('docs/json/locations_inv.json', 'w') as outfile:
    json.dump(loc, outfile)