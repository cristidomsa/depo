import json
import csv
import utils

inv = {}
loc = {}
loc_desc = {}
na_loc = []
inventory = {}

def get_loc_type(desc):
    if desc in loc_desc.keys():
        if (loc_desc[desc]['tier_type'] != 'Pick') and (loc_desc[desc]['tier_type'] != 'Reserve'):
            na_loc.append(desc)
        else:
            return loc_desc[desc]['tier_type']

with open('docs/Locations.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        loc_desc[row['Name']] = {'desc': row['DisplayName'],
                                'tier_type': row['LocationType']}

with open('docs/Inventory.csv') as f:
    reader = csv.DictReader(f)
    inventory['Inventories'] = []
    for row in reader:
        inventory['Inventories'].append(row)

# with open('docs/json/inventory.json') as f:

#     inventory = json.load(f)

for item in inventory['Inventories']:
    if item['ItemNumber'] not in inv.keys():
        inv[item['ItemNumber']] = []
    inv[item['ItemNumber']].append({'Name': item['Location'],
                                    'QTY': item['Quantity'],
                                    'tier_type': get_loc_type(item['Location'])})


for item in inventory['Inventories']:
    if item['Location'] not in loc.keys():
        loc[item['Location']] = {}
    loc[item['Location']][item['ItemNumber']] = item['Quantity']

utils._write_json('docs/json/sku_inv.json', inv)
utils._write_json('docs/json/locations_inv.json', loc)
utils._write_json('docs/json/loc_desc.json', loc_desc)


with open('docs/json/na_loc.csv', 'w') as output:
    output.write('\n'.join(list(set(na_loc))))