# Script: Reduce played time to 2 min
# Author: Alfazari911


offset=search_first_text_simple('playTime', save_data, encoding='utf-8')
offset2=search_first_text_simple(',"openingCreditsPlayed', save_data, encoding='utf-8')

distance=offset2-(offset+10)



new=offset+10

#delete_bytes(offset, length, save_data)

value = read_offset(new, save_data, length=1)
print(value)

delete_bytes(new, distance, save_data)

time=bytes.fromhex('31 37 32 2E 31 31 30 30 34 36')
insert_bytes(new, time, save_data)
