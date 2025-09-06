# Script: Max geo (money)
# Author: Alfazari911

offset=search_first_text_simple('geo', save_data, encoding='utf-8')
geo_off=offset+5
insert_bytes(geo_off, '39 39 39 39', save_data)

