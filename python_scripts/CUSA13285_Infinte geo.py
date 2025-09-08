# Script: Infinte geo
# Author: Alfazari911

offset=search_first_text_simple('geo', save_data, encoding='utf-8')
print(offset)
geo_offset=offset+5
insert_bytes(geo_offset, '39 39 39 39', save_data)
