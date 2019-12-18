# depo data generating scripts

Dependencies:

/docs/orders.csv
/docs/Locations_fixed.csv
/docs/json/inventory.json

Date selecting:
make_data.py line 12 - modify start_date, end_date (format: YYYY-MM-DD)

Running:
python3 make_data.py
python3 make_locations_py
python3 make_orders.py
