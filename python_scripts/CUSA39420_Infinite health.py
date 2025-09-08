# Script: Infinite health
# Author: Alfazari911

offset=search_first_text_simple('health', save_data, encoding='utf-8')
health_off=offset+8

insert_bytes(health_off, '39 39 39', save_data)

offset1=search_first_text_simple('maxHealth', save_data, encoding='utf-8')
max=offset1+11

insert_bytes(max, '39 39 39', save_data)

offset2=search_first_text_simple('maxHealthBase', save_data, encoding='utf-8')

base=offset2+15

insert_bytes(base, '39 39 39', save_data)
