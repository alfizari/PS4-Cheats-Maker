# Script: unlock dash
# Author: Alfazari911

offset=search_first_text_simple('hasDashSlash', save_data, encoding='utf-8')
print(offset)
unlock=offset+14
write_text_at_offset(unlock, 'true',save_data, encoding='utf-8')

extra_e_offset=offset+18
print(extra_e_offset)
delete_bytes(extra_e_offset, 1, save_data)
