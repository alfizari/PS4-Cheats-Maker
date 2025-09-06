# Script: Unlock Needle Throw
# Author: Alfazari911

offset=search_first_text_simple('hasNeedleThrow', save_data, encoding='utf-8')
offset_unlock=16+offset
print(offset_unlock)

offset_delete=20+offset
write_text_at_offset(offset_unlock, 'true',save_data, encoding='utf-8')
delete_bytes(offset_delete, 1, save_data)
