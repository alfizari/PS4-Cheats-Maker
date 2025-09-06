# Script: Max ShellShards
# Author: Alfazari911

list=search_all_text_simple('ShellShards', save_data, encoding='utf-8')

offset_shards=list[2]
print(offset_shards)
insert_bytes(offset_shards, '39 39 39 39', save_data)
