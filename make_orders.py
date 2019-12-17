import json
import csv

orders = {}
prov = {}
with  open('docs/json/locations_inv.json', 'r') as f:
    inventory = json.load(f)

def find_locations(sku):
    if sku in inventory.keys():
        return inventory[sku]

with open('docs/future_orders_normal.csv') as f:

    csvReader = csv.DictReader(f)
    for row in csvReader:
        id = row['Order#']
        date = row['Date Start']
        if date not in orders.keys():
            orders[date] = {}
        if id not in orders[date].keys(): 
            orders[date][id] = {}
        sku = row['UPC Code'].split('.')[0]
        orders[date][id][sku] = {'Customer': row['Customer #'],
                                            'QTY': row['Units Open'],
                                            'Locations': find_locations(sku)
            }
        if sku in prov.keys():
            prov[sku] += int(row['Units Open'])
        else:
            prov[sku] = int(row['Units Open'])

with open('docs/json/future_orders_normal.json', 'w') as outfile:
    json.dump(orders, outfile)

with open('docs/json/future_sku_qty.json', 'w') as outfile:
    json.dump(prov, outfile)


