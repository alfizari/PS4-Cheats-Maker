# Example JSON file: built_in_functions.json
# [
#   {"name": "search_for", "template": "offset1 = search_for(start_offset, end_offset, pattern)\n"},
#   {"name": "read_offset", "template": "value = read_offset(address)\n"},
#   {"name": "write_offset", "template": "write_offset(address, value)\n"}
# ]

# helpers.py

import struct
from typing import Union, Optional, List, Tuple


def search_for(start_offset: int, end_offset: int, pattern: Union[str, bytes], data: bytes) -> Optional[int]:
    """
    Search for a byte pattern or AOB in a byte array.
    Returns the offset if found, else None.
    """
    if isinstance(pattern, str):
        # Convert hex string to bytes, e.g., "44 16 61 00"
        pattern = bytes.fromhex(pattern.replace(" ", ""))
    idx = data.find(pattern, start_offset, end_offset)
    return idx if idx != -1 else None

def read_offset(offset: int, data: bytes, length: int = 4) -> int:
    """Read a value from data at a given offset"""
    return int.from_bytes(data[offset:offset+length], "little")

def write_offset(offset: int, value: int, data: bytearray, length: int = 4) -> None:
    """Write a value to data at a given offset"""
    data[offset:offset+length] = value.to_bytes(length, "little")

# Extended helper functions

def read_float(offset: int, data: bytes) -> float:
    """Read a 32-bit float from data at given offset"""
    return struct.unpack("<f", data[offset:offset+4])[0]

def write_float(offset: int, value: float, data: bytearray) -> None:
    """Write a 32-bit float to data at given offset"""
    data[offset:offset+4] = struct.pack("<f", value)

def read_double(offset: int, data: bytes) -> float:
    """Read a 64-bit double from data at given offset"""
    return struct.unpack("<d", data[offset:offset+8])[0]

def write_double(offset: int, value: float, data: bytearray) -> None:
    """Write a 64-bit double to data at given offset"""
    data[offset:offset+8] = struct.pack("<d", value)

def read_string(offset: int, data: bytes, length: Optional[int] = None, encoding: str = "utf-8") -> str:
    """
    Read a string from data at given offset.
    If length is None, reads until null terminator.
    """
    if length is None:
        # Find null terminator
        end = data.find(b'\x00', offset)
        if end == -1:
            end = len(data)
        return data[offset:end].decode(encoding, errors='ignore')
    else:
        return data[offset:offset+length].decode(encoding, errors='ignore').rstrip('\x00')

def write_string(offset: int, value: str, data: bytearray, max_length: Optional[int] = None, 
                 encoding: str = "utf-8", null_terminate: bool = True) -> None:
    """
    Write a string to data at given offset.
    If max_length is specified, pads or truncates as needed.
    """
    encoded = value.encode(encoding)
    if null_terminate and not encoded.endswith(b'\x00'):
        encoded += b'\x00'
    
    if max_length is not None:
        if len(encoded) > max_length:
            encoded = encoded[:max_length-1] + b'\x00' if null_terminate else encoded[:max_length]
        else:
            encoded = encoded.ljust(max_length, b'\x00')
    
    data[offset:offset+len(encoded)] = encoded

def read_bool(offset: int, data: bytes) -> bool:
    """Read a boolean (1 byte) from data at given offset"""
    return bool(data[offset])

def write_bool(offset: int, value: bool, data: bytearray) -> None:
    """Write a boolean (1 byte) to data at given offset"""
    data[offset] = 1 if value else 0

def search_all(pattern: Union[str, bytes], data: bytes) -> List[int]:
    """
    Find all occurrences of a pattern in data.
    Returns list of offsets where pattern is found.
    """
    if isinstance(pattern, str):
        pattern = bytes.fromhex(pattern.replace(" ", ""))
    
    offsets = []
    start = 0
    while True:
        idx = data.find(pattern, start)
        if idx == -1:
            break
        offsets.append(idx)
        start = idx + 1
    return offsets

def replace_pattern(pattern: Union[str, bytes], replacement: Union[str, bytes], 
                   data: bytearray, count: int = -1) -> int:
    """
    Replace pattern with replacement in data.
    Returns number of replacements made.
    """
    if isinstance(pattern, str):
        pattern = bytes.fromhex(pattern.replace(" ", ""))
    if isinstance(replacement, str):
        replacement = bytes.fromhex(replacement.replace(" ", ""))
    
    if len(pattern) != len(replacement):
        raise ValueError("Pattern and replacement must be same length")
    
    replacements = 0
    start = 0
    while count != 0:
        idx = data.find(pattern, start)
        if idx == -1:
            break
        data[idx:idx+len(pattern)] = replacement
        replacements += 1
        start = idx + len(pattern)
        count -= 1
    
    return replacements

def create_backup(data: bytes, filename: str = "backup.sav") -> None:
    """Create a backup of the save data"""
    with open(filename, "wb") as f:
        f.write(data)

def load_save_file(filename: str) -> bytearray:
    """Load a save file into a mutable bytearray"""
    with open(filename, "rb") as f:
        return bytearray(f.read())

def save_file(filename: str, data: bytearray) -> None:
    """Save bytearray data to file"""
    with open(filename, "wb") as f:
        f.write(data)

def get_checksum_crc32(data: bytes, start: int = 0, end: Optional[int] = None) -> int:
    """Calculate CRC32 checksum of data range"""
    import zlib
    end = end or len(data)
    return zlib.crc32(data[start:end]) & 0xffffffff

def get_checksum_md5(data: bytes, start: int = 0, end: Optional[int] = None) -> bytes:
    """Calculate MD5 checksum of data range"""
    import hashlib
    end = end or len(data)
    return hashlib.md5(data[start:end]).digest()

def get_checksum_md5_hex(data: bytes, start: int = 0, end: Optional[int] = None) -> str:
    """Calculate MD5 checksum of data range as hex string"""
    import hashlib
    end = end or len(data)
    return hashlib.md5(data[start:end]).hexdigest()

def get_checksum_sha1(data: bytes, start: int = 0, end: Optional[int] = None) -> bytes:
    """Calculate SHA-1 checksum of data range"""
    import hashlib
    end = end or len(data)
    return hashlib.sha1(data[start:end]).digest()

def get_checksum_sha1_hex(data: bytes, start: int = 0, end: Optional[int] = None) -> str:
    """Calculate SHA-1 checksum of data range as hex string"""
    import hashlib
    end = end or len(data)
    return hashlib.sha1(data[start:end]).hexdigest()

def verify_checksum(data: bytes, expected_checksum: Union[int, bytes, str], checksum_offset: int,
                   data_start: int = 0, data_end: Optional[int] = None, 
                   checksum_type: str = "crc32") -> bool:
    """
    Verify if data matches expected checksum.
    Excludes the checksum bytes themselves from calculation.
    
    Args:
        checksum_type: "crc32", "md5", "md5_hex", "sha1", or "sha1_hex"
    """
    # Create data without checksum for verification
    temp_data = bytearray(data)
    
    if checksum_type == "crc32":
        temp_data[checksum_offset:checksum_offset+4] = b'\x00\x00\x00\x00'
        calculated = get_checksum_crc32(temp_data, data_start, data_end)
    elif checksum_type == "md5":
        temp_data[checksum_offset:checksum_offset+16] = b'\x00' * 16
        calculated = get_checksum_md5(temp_data, data_start, data_end)
    elif checksum_type == "md5_hex":
        temp_data[checksum_offset:checksum_offset+32] = b'\x00' * 32
        calculated = get_checksum_md5_hex(temp_data, data_start, data_end)
    elif checksum_type == "sha1":
        temp_data[checksum_offset:checksum_offset+20] = b'\x00' * 20
        calculated = get_checksum_sha1(temp_data, data_start, data_end)
    elif checksum_type == "sha1_hex":
        temp_data[checksum_offset:checksum_offset+40] = b'\x00' * 40
        calculated = get_checksum_sha1_hex(temp_data, data_start, data_end)
    else:
        raise ValueError(f"Unsupported checksum type: {checksum_type}")
    
    return calculated == expected_checksum

def update_checksum(data: bytearray, checksum_offset: int, 
                   data_start: int = 0, data_end: Optional[int] = None,
                   checksum_type: str = "crc32") -> None:
    """
    Calculate and update checksum in the data.
    Excludes the checksum bytes themselves from calculation.
    
    Args:
        checksum_type: "crc32", "md5", "md5_hex", "sha1", or "sha1_hex"
    """
    if checksum_type == "crc32":
        # Zero out checksum area first
        data[checksum_offset:checksum_offset+4] = b'\x00\x00\x00\x00'
        # Calculate new checksum
        checksum = get_checksum_crc32(data, data_start, data_end)
        # Write checksum back
        write_offset(checksum_offset, checksum, data, 4)
    
    elif checksum_type == "md5":
        # Zero out checksum area first
        data[checksum_offset:checksum_offset+16] = b'\x00' * 16
        # Calculate new checksum
        checksum = get_checksum_md5(data, data_start, data_end)
        # Write checksum back
        data[checksum_offset:checksum_offset+16] = checksum
    
    elif checksum_type == "md5_hex":
        # Zero out checksum area first
        data[checksum_offset:checksum_offset+32] = b'\x00' * 32
        # Calculate new checksum
        checksum = get_checksum_md5_hex(data, data_start, data_end)
        # Write checksum back
        data[checksum_offset:checksum_offset+32] = checksum.encode('ascii')
    
    elif checksum_type == "sha1":
        # Zero out checksum area first
        data[checksum_offset:checksum_offset+20] = b'\x00' * 20
        # Calculate new checksum
        checksum = get_checksum_sha1(data, data_start, data_end)
        # Write checksum back
        data[checksum_offset:checksum_offset+20] = checksum
    
    elif checksum_type == "sha1_hex":
        # Zero out checksum area first
        data[checksum_offset:checksum_offset+40] = b'\x00' * 40
        # Calculate new checksum
        checksum = get_checksum_sha1_hex(data, data_start, data_end)
        # Write checksum back
        data[checksum_offset:checksum_offset+40] = checksum.encode('ascii')
    
    else:
        raise ValueError(f"Unsupported checksum type: {checksum_type}")

def hex_dump(data: bytes, offset: int = 0, length: int = 256, bytes_per_line: int = 16) -> str:
    """
    Create a hex dump of data for debugging.
    Useful for analyzing save file structure.
    """
    lines = []
    end = min(offset + length, len(data))
    
    for i in range(offset, end, bytes_per_line):
        line_data = data[i:i+bytes_per_line]
        
        # Hex representation
        hex_part = ' '.join(f'{b:02x}' for b in line_data)
        hex_part = hex_part.ljust(bytes_per_line * 3 - 1)
        
        # ASCII representation
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in line_data)
        
        lines.append(f'{i:08x}: {hex_part} |{ascii_part}|')
    
    return '\n'.join(lines)

def find_value_offset(value: int, data: bytes, length: int = 4, 
                     start: int = 0, end: Optional[int] = None) -> List[int]:
    """
    Find all offsets where a specific integer value appears in the data.
    Useful for locating specific stats or values in save files.
    """
    end = end or len(data)
    value_bytes = value.to_bytes(length, "little")
    offsets = []
    
    current = start
    while current <= end - length:
        if data[current:current+length] == value_bytes:
            offsets.append(current)
        current += 1
    
    return offsets

def read_array(offset: int, data: bytes, count: int, element_size: int = 4) -> List[int]:
    """Read an array of integers from data"""
    result = []
    for i in range(count):
        pos = offset + (i * element_size)
        result.append(read_offset(pos, data, element_size))
    return result

def write_array(offset: int, values: List[int], data: bytearray, element_size: int = 4) -> None:
    """Write an array of integers to data"""
    for i, value in enumerate(values):
        pos = offset + (i * element_size)
        write_offset(pos, value, data, element_size)

# Convenience functions for common data types
def read_byte(offset: int, data: bytes) -> int:
    """Read a single byte (unsigned)"""
    return data[offset]

def write_byte(offset: int, value: int, data: bytearray) -> None:
    """Write a single byte"""
    data[offset] = value & 0xFF

def read_short(offset: int, data: bytes) -> int:
    """Read a 16-bit integer"""
    return read_offset(offset, data, 2)

def write_short(offset: int, value: int, data: bytearray) -> None:
    """Write a 16-bit integer"""
    write_offset(offset, value, data, 2)

def read_int(offset: int, data: bytes) -> int:
    """Read a 32-bit integer (alias for read_offset)"""
    return read_offset(offset, data, 4)

def write_int(offset: int, value: int, data: bytearray) -> None:
    """Write a 32-bit integer (alias for write_offset)"""
    write_offset(offset, value, data, 4)

def read_long(offset: int, data: bytes) -> int:
    """Read a 64-bit integer"""
    return read_offset(offset, data, 8)

def write_long(offset: int, value: int, data: bytearray) -> None:
    """Write a 64-bit integer"""
    write_offset(offset, value, data, 8)