import pandas as pd

orders = pd.read_csv('docs/orders.csv', header=0, index_col=6, usecols=[1,2,3,4,5,9,10,13], parse_dates=True)
locations = pd.read_csv('docs/Locations_fixed.csv', header=0, index_col=0)

inventory = pd.read_csv('docs/Inventory.csv', header=0, index_col=1, usecols=[0,1,2])

products_box_size = pd.read_csv('docs/icboxd_Box_Detail.csv', header=0, index_col=0, usecols=[1,2])

inventory_per_locations = pd.merge(locations, inventory, left_index=True, right_index=True)

def get_orders(start_date='2020-03-01', end_date='2020-03-31'):

    return orders.loc[start_date:end_date]

inventory_per_locations.to_csv('docs/inventory_per_locations.csv')

available_locations = set(locations.index.unique().tolist()) - set(inventory_per_locations.index.unique().tolist())
orders_march = get_orders()


f = {'Units Open':'sum',
    'UPC Code': 'unique'}

g = {'ICBD_QTY':'max',
    'ICBD_UPC': 'unique'}

is_web = orders_march['Customer #'] == 'KU40'
is_normal = orders_march['Customer #'] != 'KU40'


orders_march.to_csv('docs/future_orders.csv')
orders_march[is_normal].to_csv('docs/future_orders_normal.csv')
orders_march[is_web].to_csv('docs/future_orders_web.csv')


sku_orders = orders_march[is_normal].reset_index(drop=False).groupby('UPC Code').agg(f).set_index('UPC Code')
product_max_box = products_box_size.reset_index(drop=False).groupby('ICBD_UPC').agg(g).set_index('ICBD_UPC')
product_max_box.index = product_max_box.index.map(int)
sku_orders.index = sku_orders.index.map(int)

products_cycles = pd.merge(sku_orders, product_max_box, left_index=True, right_index=True)

products_cycles['Cycles'] = products_cycles['Units Open'] / products_cycles['ICBD_QTY'] 

products_cycles.to_csv('docs/products_cycles_normal.csv', index_label='SKU')

# orders_march[is_web].to_csv('docs/orders-march-web.csv')
# orders_march[is_normal].to_csv('docs/orders-march-normal.csv')


