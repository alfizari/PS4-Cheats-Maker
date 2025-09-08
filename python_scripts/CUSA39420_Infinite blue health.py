# Script: Infinite blue health
# Author: Alfazari911

offset=search_first_text_simple('healthBlue', save_data, encoding='utf-8')
health_off=offset+12

insert_bytes(health_off, '39 39 39', save_data)


