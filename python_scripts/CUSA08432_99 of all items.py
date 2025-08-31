# Script: 99 of all items
# Author: Alfazari911

start_pattern="A0 BB 0D 00" # Where I want to start the search
start_offset = search_for(0xA06, 0x2000, start_pattern, save_data) #Finding that pattern
print(start_offset) # Debug

end_pattern="FF FF FF FF FF FF FF FF" # Where to end
end_offset = search_for(0xA60, 0x2000, end_pattern, save_data) #finding that pattern end
print('ends at', end_offset) # Debug
start_offset=start_offset+4 #Alignment 
write_offset_loop(start_offset, end_offset, 28, 99, save_data, length= 1)
# This will replace the value at start offset, then move 28 bytes and write the same value there 
#until the end

