# Script: Unlock white key
# Author: Alfazari911

offset=search_first_text_simple('hasWhiteKey', save_data, encoding='utf-8')
unlock_key_offset=offset+13
write_text_at_offset(unlock_key_offset, 'true',save_data, encoding='utf-8')

last_e=offset+17
delete_bytes(last_e, 1, save_data)
