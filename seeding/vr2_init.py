from datetime import datetime
import struct

from utils import index_by, resign_seeds, store_at_index, str_to_bytes

def create_seed_array_1(seed0: int = 0x1571, seed1: int = 1):
    result_arr = bytearray()
    
    for i in range(0, 0x9BC, 4):
        seed0 = seed1 + ((0x6C078965 * (seed0 ^ (seed0>>30))) & 0xFFFFFFFF)
        seed0 &= 0xFFFFFFFF
        seed1 += 1
        result_arr.extend(struct.pack("<I", seed0))
        if i >= 0x9BC -4:
            print(hex(seed0))
    
    print(hex(seed1))
    return result_arr

def update_array_1(array_1: bytearray):
    raise NotImplementedError(f"Not Yet reversed. MK11.exe+B930CC")

def create_seed_array_2():
    v21 = []
    v2 = 1e-7
    _double = 2791064867574.0
    _time_multiplier = v2 * _double

    ts = int(datetime.now().timestamp()) & 0xFFFFFFFF
    ts = 0x67D13558 # For reproduce
    ts *= _time_multiplier
    ts = int(ts)
    ts = 0x1BD17917146FB  # For reproduce
    ts = int(ts) & 0xFFFFFFFF
    v21.append(ts)
    # Random generation script, for reproducability I'm gonna static them
    for r in [
        0x22DFE792,
        0xDE431285,
        0x02DAC477,
        0x84B0AF21,
        0xEB3A955E,
        0x8A5E4C96,
        0x5F4E54ED,
    ]:
        v21.append(r & 0xFFFFFFFF)

    v4 = v6 = v19 = 0
    v5 = v21
    # for i in range(len(v21)): # idk what this is doing. It seems to be copying the values but sometimes it's not
    #     if v4 == v6:
    #         something = sub_7ff7B60D25B0(v6, v5)
    #         v4 = v19
    #         v6 = something + 1 # idk # v6 is the location of the next index, can be ignored
    #     else:
    #         v6 = v5[i]
    #         v6 += 4
    #         # idk = v6

    v23 = bytearray()

    B16DA0_CreateRandomArray(v21, v23, 0x9C0) # v24 was only used as maximum size
    # with open("v23.bin", "wb") as f:
    #     f.write(v23)

def B16DA0_CreateRandomArray(seeds, some_memory, size):
    elements_count = (size >> 2) & 0xFFFFFFFF # Elements count of some_memory, number of ints
    if not size:
        return
    
    random_seeds_length = (len(seeds) * 4) >> 2 # distance between seeds 0 and 1, idk how else to get the value from. I assume it's size of seeds
    random_seeds_length &= 0xFFFFFFFF
    # v5 is now len(seeds)
    if elements_count < 0x26F:
        if elements_count < 0x44:
            if elements_count < 0x27:
                if elements_count < 7:
                    v6 = (elements_count - 1) >> 1
                else:
                    v6 = 3
            else:
                v6 = 5
        else:
            v6 = 7
    else:
        v6 = 11

    v7 = random_seeds_length + 1
    v8 = (elements_count - v6) >> 1
    v9 = v32 = v8 + v6
    if elements_count > random_seeds_length:
        v7 = elements_count

    a2 = some_memory
    for _ in range(elements_count):
        some_memory.extend(struct.pack("<I", 0x8B8B8B8B))
    
    loop_counter = 0
    if (v7):
        # do
        while (loop_counter < v7):
            v13 = (loop_counter + v8) % elements_count
            v14 = index_by(a2, v13)
            v15_idx = loop_counter % elements_count
            v15 = index_by(a2, v15_idx)
            temp = index_by(a2, (loop_counter - 1) % elements_count)
            v16 = 0x19660D * (v15 ^ v14 ^ temp ^ ((v15 ^ v14 ^ temp) >> 27))
            v16 &= 0xFFFFFFFF
            if loop_counter:
                if loop_counter > random_seeds_length:
                    v17 = loop_counter % elements_count
                else:
                    idx = (loop_counter-1)%random_seeds_length
                    v17 = loop_counter % elements_count + seeds[idx]
                    v17 &= 0xFFFFFFFF
            else:
                v17 = random_seeds_length
            v18 = v17 + v16
            v18 &= 0xFFFFFFFF
            store_at_index(a2, v13, (v14 + v16) & 0xFFFFFFFF)
            v19 = loop_counter + v32
            v19 &= 0xFFFFFFFF
            loop_counter += 1
            loop_counter &= 0xFFFFFFFF
            store_val = index_by(a2, v19 % elements_count) + v18
            store_val &= 0xFFFFFFFF
            store_at_index(a2, v19 % elements_count, store_val)
            store_at_index(a2, v15_idx, v18)

        v9 = v32

    v20 = elements_count + v7
    v20 &= 0xFFFFFFFF
    if loop_counter < v20:
        v21 = loop_counter - 1
        v22 = v8 + 1
        v23 = v9 + 1
        v21, v22, v23 = resign_seeds(v21, v22, v23)
        v30 = v20 - 1 # Should start with a do while, but python doesn't support it, so I need to make sure I can enter
        while v30 < v20:
            v24 = ((v22 + v21)&0xFFFFFFFF) % elements_count
            v25 = index_by(a2, v24)
            v26_idx = v24
            v27 = (v21 + 1) & 0xFFFFFFFF
            v27 %= elements_count
            temp1 = index_by(a2, v27)
            temp2 = index_by(a2, v21 % elements_count)
            temp_val = v25 + temp1 + temp2
            temp_val &= 0xFFFFFFFF
            v28 = 0x5D588B65 * (temp_val ^ (temp_val >> 27))
            v28 &= 0xFFFFFFFF
            v29 = (v23 + v21) & 0xFFFFFFFF
            v29 %= elements_count
            v30 = v21 + 2
            v21 += 1
            store_at_index(a2, v26_idx, v28 ^ v25)
            store_at_index(a2, v29, index_by(a2, v29) ^ ((v28 - v27) & 0xFFFFFFFF))
            store_at_index(a2, v27, (v28 - v27) & 0xFFFFFFFF)


if __name__ == "__main__":
    # result = create_array_1(0x1571, 1)
    # print(result[:4])
    create_seed_array_2()
