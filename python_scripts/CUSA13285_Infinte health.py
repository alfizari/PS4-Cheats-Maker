# Script: Infinte health
# Author: Alfazari911

offset=search_first_text_simple('health', save_data, encoding='utf-8')
print(offset)
health_offset=offset+8
write_text_at_offset(health_offset, '9',save_data, encoding='utf-8')
insert_bytes(health_offset, '39 39 39', save_data)


offset1=search_first_text_simple('maxHealth', save_data, encoding='utf-8')
maxhealth=offset1+11
write_text_at_offset(maxhealth, '9',save_data, encoding='utf-8')
insert_bytes(maxhealth, '39 39 39', save_data)

offset2=search_first_text_simple('maxHealthBase', save_data, encoding='utf-8')
maxhealthbase=offset2+15
write_text_at_offset(maxhealthbase, '9',save_data, encoding='utf-8')
insert_bytes(maxhealthbase, '39 39 39', save_data)
