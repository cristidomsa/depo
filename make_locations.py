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
        tier = loc_desc[desc].split('-')[-2]
        if int(tier) in [9,10,11]:
            return 'P'
        else:
            return 'R'
    else:
        na_loc.append(desc)
        return 'NA'

with open('docs/Locations_fixed.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        loc_desc[row['Name']] = row['DisplayName']

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
    output.write(','.join(list(set(na_loc))))