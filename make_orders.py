
import json
import csv
import datetime
import utils

HEADER = ["SKU", "Total Normal", "Total KU40", "Total Web", "Items pickable", "Count pickable locations", "Items on pallets", "Count pallets locations", "down minus needed"]

orders = {}
orders_ids = []
prov = {}
sku_web = {}

def _get_customer_type(customer):
    if customer == 'KU40':
        return 'reserved'
    elif customer.strip().startswith('KU'):
        return 'web'
    else:
        return 'normal'

def _get_qty_per_type(dates, order_type):
    cnt = 0
    for order in dates:
        if order['type'] == order_type:
            cnt += order['QTY']

    return cnt

def _get_orders_by_date(start_date, end_date):
    datetime.datetime.strftime()

def add_web_orders():
    orders_web = utils._read_json('docs/json/orders.json')

    for order in orders_web:
        if str(order['Id']) not in orders_ids and order['CustomerNumber'].startswith('KU'):
            for sku in order['OrderDetails']:
                if sku['ItemNumber'] in sku_web.keys():
                    sku_web[sku['ItemNumber']] += sku['Quantity']
                else:
                    sku_web[sku['ItemNumber']] = sku['Quantity']


def find_locations(sku):
    if sku in inventory.keys():
        return inventory[sku]

def make_status():
    status = []
    for sku, data in prov.items():
        line = []
        items_down = 0
        items_up = 0
        items_na = 0
        count_up = 0
        count_down = 0
        count_na = 0
        if data['Locations'] is None:
            continue
        for loc in data['Locations']:
            if loc['tier_type'] == "Pick":
                items_down += int(loc['QTY'])
                count_down += 1
            elif loc['tier_type'] == "Reserve":
                items_up += int(loc['QTY'])
                count_up += 1
            elif loc['tier_type'] == None:
                items_na += int(loc['QTY'])
                count_na += 1
        
        line.append(sku)
        line.append(data['QTY_normal'])
        line.append(data['QTY_KU40'])
        if sku in sku_web.keys():
            qty_web = _get_qty_per_type(data['Dates'], "web") + sku_web[sku]
        else:
            qty_web = _get_qty_per_type(data['Dates'], "web")
        line.append(_get_qty_per_type(data['Dates'], "web"))

        line.append(items_down)
        line.append(count_down)
        line.append(items_up)
        line.append(count_up)

       # line.append(items_na)
        #line.append(count_na)

        line.append(items_down - data['QTY_normal'] - data['QTY_KU40'] + qty_web)
        status.append(line)
    
    with open('status.csv','w') as f:
        f.write(",".join(HEADER))
        f.write('\n')
        for line in status:
            f.write(",".join(map(str,line)))
            f.write('\n')

inventory = utils._read_json('docs/json/sku_inv.json')

loc_desc = utils._read_json('docs/json/loc_desc.json')

orders_web = utils._read_json('docs/json/orders.json')

with open('docs/future_orders.csv') as f:

    csvReader = csv.DictReader(f)
    for row in csvReader:
        id = row['Order#']
        if id not in orders_ids:
            orders_ids.append(id)
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
        if int(row['Units Open']) > 0:
            if sku not in prov.keys():
                prov[sku] = {}
                if row['Customer #'] == 'KU40':
                    prov[sku]['QTY_KU40'] = int(row['Units Open'])
                    prov[sku]['QTY_normal'] = 0
                else:
                    prov[sku]['QTY_normal'] = int(row['Units Open'])
                    prov[sku]['QTY_KU40'] = 0
                prov[sku]['Locations'] = find_locations(sku)
                prov[sku]['Dates'] = []
            else:
                if row['Customer #'] == 'KU40':
                    prov[sku]['QTY_KU40'] += int(row['Units Open'])
                else:
                    prov[sku]['QTY_normal'] += int(row['Units Open'])
            
            prov[sku]['Dates'].append({'date': row['Date Start'],
                                        'id': id,
                                        'QTY': int(row['Units Open']),
                                        'type': _get_customer_type(row['Customer #'])})

add_web_orders()
make_status()

with open('docs/json/future_orders.json', 'w') as outfile:
    json.dump(orders, outfile)

with open('docs/json/future_sku_qty.json', 'w') as outfile:
    json.dump(prov, outfile)


