-- ============================================
-- Lua Cheat Starter for Save Editor
-- Preloaded Helpers: Byte, UInt16, UInt32, AOB Search
-- ============================================

-- ===== Helper Functions =====

-- Read a single byte
function read_byte(offset)
    return save.data[offset + 1]
end

-- Write a single byte
function write_byte(offset, value)
    save.data[offset + 1] = value
end

-- Read 16-bit little-endian integer
function read_uint16(offset)
    local b1 = save.data[offset + 1]
    local b2 = save.data[offset + 2]
    return b1 + b2 * 256
end

-- Write 16-bit little-endian integer
function write_uint16(offset, value)
    save.data[offset + 1] = value % 256
    save.data[offset + 2] = math.floor(value / 256) % 256
end

-- Read 32-bit little-endian integer
function read_uint32(offset)
    local b1 = save.data[offset + 1]
    local b2 = save.data[offset + 2]
    local b3 = save.data[offset + 3]
    local b4 = save.data[offset + 4]
    return b1 + b2*256 + b3*65536 + b4*16777216
end

-- Write 32-bit little-endian integer
function write_uint32(offset, value)
    save.data[offset + 1] = value % 256
    save.data[offset + 2] = math.floor(value / 256) % 256
    save.data[offset + 3] = math.floor(value / 65536) % 256
    save.data[offset + 4] = math.floor(value / 16777216) % 256
end

-- Search for a single byte value
function find_value(value)
    local offsets = {}
    for i = 1, #save.data do
        if save.data[i] == value then
            table.insert(offsets, i - 1)  -- 0-based
        end
    end
    return offsets
end

-- =============================
-- Array of Bytes (AOB) Search
-- pattern: table of bytes, use nil for wildcard
function find_pattern(pattern)
    local matches = {}
    local plen = #pattern
    local data_len = #save.data

    for i = 1, data_len - plen + 1 do
        local match = true
        for j = 1, plen do
            if pattern[j] ~= nil and save.data[i + j - 1] ~= pattern[j] then
                match = false
                break
            end
        end
        if match then
            table.insert(matches, i - 1)  -- 0-based
        end
    end
    return matches
end

-- Apply all changes back to the save file
function apply()
    write_back(save)
end
exmpl 
we first define a few helper functions to read and write bytes and integers. Then we provide functions to search for values and patterns. Finally, we have an apply function that writes back any changes made to the save data.
-- Write a single byte at a given offset
function write_byte(offset, value)
    save.data[offset] = value
end

function apply()
    -- Example: write 11 at offset 0x1000
    write_byte(0x1000, 1)
    write_back(save)
end

apply()
-- ===== Example Usage =====
-- Modify single byte
-- write_byte(0x102, 22)

-- Modify 16-bit integer
-- write_uint16(0x104, 300)

-- Modify 32-bit integer
-- write_uint32(0x108, 12345678)

-- Search for a value
-- local offsets = find_value(99)
-- for _, off in ipairs(offsets) do
--     print(string.format("Found 99 at 0x%X", off))
-- end

-- Search for a pattern (0x12 0x34 any byte 0x56)
-- local offsets = find_pattern({0x12, 0x34, nil, 0x56})
-- for _, off in ipairs(offsets) do
--     print(string.format("Pattern found at 0x%X", off))
-- end

-- Apply changes
-- apply()

