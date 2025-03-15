from datetime import datetime
import struct
from typing import Literal, Union

from utils import compare_bytearrays, index_by, resign_seeds, store_at_index, dump, PYMEM_ENABLED
if PYMEM_ENABLED:
    from utils import compare_memory, dump_memory

def initialize_state(seed):
    result_arr = bytearray()

    for i in range(1, 0x9C0 // 4):
        seed = i + ((1812433253 * (seed ^ (seed >> 30))) & 0xFFFFFFFF)
        seed &= 0xFFFFFFFF
        result_arr.extend(struct.pack("<I", seed))

    GLOBAL_ARRAY[3] = result_arr  # Or can directly edit the array by indexing at seed1
    GLOBAL_ARRAY[1] = 0x270

    return GLOBAL_ARRAY


def update_array_1(array_1: bytearray):
    raise NotImplementedError(f"Not Yet reversed. MK11.exe+B930CC")

def recreate_seed_array_1():
    global GLOBAL_ARRAY
    GLOBAL_ARRAY[0] = 1
    v21 = []
    v2 = 1e-7
    _double = 0x41987E9DB71
    _time_multiplier = v2 * _double

    ts = int(datetime.now().timestamp()) & 0xFFFFFFFF
    ts = 0x0000000067D3D3A7  # For reproduce
    ts *= _time_multiplier
    ts = int(ts) & 0xFFFFFFFF
    ts = 0x84AC2951
    v21.append(ts)
    # Random generation script, for reproducability I'm gonna static them
    for r in [
        0x00000000C921BAD3,
        0x00000000629F23FB,
        0x0000000021A1E46F,
        0x00000000FB9B121F,
        0x0000000026366388,
        0x000000008BB37CD1,
        0x000000006A1858D5,
    ]:
        v21.append(r & 0xFFFFFFFF)

    v7 = 0

    v23 = B16DA0_CreateRandomArray(v21, 0x9C0) # v24 was only used as maximum size

    new_array = bytearray(0x9C0-4)
    for v8 in range(0x270): # Seems to be shifting everything backwards # Update: It is actually copying v23 into the global array proper index -1, -1 cuz 0x9C0 is actually greate than the size by 1
        v10 = index_by(v23, v8)
        if v8 == 0:
            GLOBAL_ARRAY[2] = v10 # before this, it was 0x1571 which is seed0 of create_seed_array_1
        else:
            store_at_index(new_array, v8 - 1, v10)
        v11 = v7 | v10
        v7 = v10 >> 31
        if v8:
            v7 = v11
    # Instead of all this, I can do global array 2 = first element, shift everything backwards once, and then store that

    GLOBAL_ARRAY[3] = new_array

    if v7 == 0:
        GLOBAL_ARRAY[2] = -1 & 0xFFFFFFFF
    GLOBAL_ARRAY[1] = 0x270

    result_array = B17320_CreateRandomArray2(2_000_000, 4)
    
    __store_global_array(0x272*2, result_array)


def B17320_CreateRandomArray2(array_size: int, element_size: int):
    seed_idx = 1
    XOR_Seeds = [
        0, 0, 0, 0 # 4 bytes each
    ]
    params_array = [
        XOR_Seeds, # 0x00 # XOR Struct
        0, # PreviousHashPtr, # 0x08
        0, # PreviousHashPtr, # 0x10
        0, # 0x18 # XOR Seed
        0, # 0x1C # Unused
        bytearray(array_size), # 0x20 # XOR Randoms Array
        array_size, # 0x28 # Seed Array Length
        
    ]
    v9_idx = 3 # 0x18 -> XOR Seed
    xor_randoms_array = params_array[5] # 0x20

    if (array_size % 16) or array_size < 100_000 or element_size > 20:
        return params_array

    params_array[6] = array_size # Redundant

    array_elements_count = array_size // 4

    for v10 in range(array_elements_count):  
        store_at_index(xor_randoms_array, v10, B190B0(seed_idx))

    v12 = v13 = 0
    if __sign_32b_int_cmp(element_size) >= 0:
        v14 = (array_size // element_size - 20) // 2
        v15 = array_size - 20
        while True:
            v27 = B190B0(seed_idx)
            v12 += v14 + v27 % v14 + 0x14
            v67 = v12

            if v12 > v15:
                return params_array
            v28 = params_array[1]  # next XOR index
            if params_array[2] == v28:
                # Generate XOR Seed Array Element
                _328730(params_array, v28, v67) 
                v12 = v67
            else:
                v28 = v12  # content of v28
                params_array[
                    2
                ] += 1  # Basically changes the index to be the next one of the XORStruct, change later!

            v13 += 1
            if v13 >= __sign_32b_int_cmp(element_size):
                v9_idx = 3  # Address into params_array -> XORSeed
                break

    if __sign_32b_int_cmp((4 * element_size) & 0xFFFFFFFF) > 0:
        v29 = 4 * element_size
        v29 &= 0xFFFFFFFF
        
        for _ in range(v29):
            v43 = B190B0(seed_idx) % element_size
            v55 = B190B0(seed_idx) % element_size
            if v43 != v55: # Swap XOR inside
                v56 = params_array[0][v55]
                v57 = params_array[0][v43]
                
                params_array[0][v43] = v56
                params_array[0][v55] = v57

        v59 = B190B0(seed_idx)
        params_array[v9_idx] = v59
        s_size = __sign_32b_int_cmp(element_size)
        if s_size > 0 and element_size >= 0x10: # Should never enter!
            raise ValueError(f"Element size was >= 10 which should never happen!")
            v61 = _mm_shuffle_epi32(_mm_cvtsi32_si128(v59), 0) # idk
            v62 = 0 # params_array[0] # index into params_array
            v63 = params_array[0][element_size-1]
            # TODO: Some weird address comparison is happening here idk if it should even enter or not!
            v8 = 0
            if False:
                v64 = 0x20
                while v8 < element_size - (element_size % 16): # the indxing below should be params_array[v62+v64-wtv]
                    # *(__m128i *)(v64 + v62 - 32) = _mm_xor_si128(v61, _mm_loadu_si128((const __m128i *)(v64 + v62 - 0x20)));
                    # *(__m128i *)(v64 + v62 - 16) = _mm_xor_si128(v61, _mm_loadu_si128((const __m128i *)(v64 + v62 - 0x10)));
                    # *(__m128i *)(v64 + v62) = _mm_xor_si128(v61, _mm_loadu_si128((const __m128i *)(v64 + v62)));
                    # *(__m128i *)(v64 + v62 + 16) = _mm_xor_si128(v61, _mm_loadu_si128((const __m128i *)(v64 + v62 + 0x10)));
                    v60 += 0x10
                    v8 += 0x10
                    v64 += 0x40

        v60 = 0
        for v60 in range(0, element_size):
            params_array[0][v60] ^= params_array[v9_idx]

    return params_array

def _328730(params_array, result_index, initial_value):
    v7 = params_array[1] # index to compare against
    v8 = v7 + 1 # index 1
    v9 = params_array[2] # 0 >> 2 # Distance between 2nd pointer and XOR arr [2] and [0]
    v10 = v9 >> 1
    if v9 <= 0x3FFFFFFFFFFFFFFF - v10:
        v11 = v10 + v9
        if v11 < v8:
            v11 = v8
    else:
        v11 = v8    

    v12 = v13 = v11 * 4
    if v11 > 0x3FFFFFFFFFFFFFFF:
        raise ValueError(f"v11 is too big!")
    if v13 == 0:
        raise ValueError(f"v13 was 0. Something went wrong! (Will cause infinite recursion)")
    if v13 < 0x1000:
        pass # Do nothing since it should go fine # The pass is there so I can track it in ida if I need
        # v16 = [[]] * v11 # Array of size 4 # Not needed since I can directly modify my memory
    else:
        raise NotImplementedError(f"This area is not tested! Erroring so you can trace!")
        # This area should never execute since v13 is always < 0x1000
        v14 = v13 + 39
        if __sign_32b_int_cmp(v14) <= v13: # Integer overflow
            raise ValueError(f"Got a negative v14!")

        v15 = [[]]*(v14//4) # Another array allocate # Convert this into an array, assume each element is of size 4
        # v16 = 32//4 # 39 & 0xE0 # 32
        # v16[24//4] = v15 # This should be relative to the content of v15 so remake later!
        v15[6] = v15 # Wrong index, should be re-calculated to see if -1 means 32 -8 or -4
        v16 = v15[7] 

    params_array[0][result_index] = initial_value
    params_array[1] = v8
    params_array[2] = v12//4
    return result_index # address of the params_array[0] index -> params_array[0][v6]


def __sign_32b_int_cmp(value: int, mask_size: int = 4):
    mask = mask_size * 8
    mask = 1 << mask
    mask -= 1
    value &= mask
    limit = 1 << 31 # 0x80000000
    if value >= limit: # Negative
        return -value
    return value

def __idx_global_array(index: int, offset):
    off_idx = index + offset
    if off_idx < 3:
        index_array = GLOBAL_ARRAY
        return index_array, off_idx
    elif off_idx < 0x26F + 3:
        index_array = GLOBAL_ARRAY[3]
        return index_array, off_idx - 3
    elif 0x270 + 0x26F + 3 > off_idx >= 0x26F + 3: # Once fixed, 270 becomes 26F
        index_array = GLOBAL_ARRAY[4]
        return index_array, off_idx - 3 - 0x26F
    else:
        idx = off_idx - 0x270 - 0x26F + 2  # 2 for the 0x272 and 0x26F indices
        if idx > len(GLOBAL_ARRAY):
            raise IndexError(f"Index {idx} is out of Global Array's range")
        index_array = GLOBAL_ARRAY
        if idx > 7:
            idx -= 1 # element 7 is ptr -> size 8. This indexing assumes size 4.
        return index_array, idx


def __store_global_array(index: int, value, offset: int = 0):
    index_array, index = __idx_global_array(index, offset)
    if isinstance(index_array, bytearray):
        store_at_index(index_array, index, value)
    else:
        index_array[index] = value


def __index_by_global_array(index: int, offset: int = 0):
    index_array, index = __idx_global_array(index, offset)
    if isinstance(index_array, bytearray):
        return index_by(index_array, index)
    else:
        return index_array[index]

def __heavy_xor_complex(initial_index, range_: int, index_offset,
    xor_idx: Union[Literal[1], Literal[2]], and_idx: Union[Literal[1], Literal[2]],
    store_offset, idx_1_offset: int, idx_2_offset: int):

    for _ in range(range_):
        idx_1 = __index_by_global_array(initial_index + idx_1_offset)
        idx_2 = __index_by_global_array(initial_index + idx_2_offset)
        if xor_idx == 1:
            l_xor = idx_1
        else:
            l_xor = idx_2
        if and_idx == 1:
            l_and = idx_1
        else:
            l_and = idx_2

        temp_xor = idx_1 ^ idx_2
        store_val_l = ((l_xor ^ temp_xor & 0x7FFFFFFF) >> 1) ^ __index_by_global_array(
            initial_index + index_offset
        )
        store_val_r = 0
        if (l_and & 1) != 0:
            store_val_r = 0x9908B0DF

        __store_global_array(initial_index + store_offset, store_val_l ^ store_val_r)

        initial_index += 1

def B190B0(seed_idx: int):
    v3 = __index_by_global_array(seed_idx)
    if v3 == 0x270: # Array 2
        # __heavy_xor_complex(seed_idx +2, 0x270, 0x18C, 2, 1, 0x26F, 0, -1)
        __heavy_xor_complex(seed_idx + 1, 0x270, 0x18D, 1, 2, 0x270, 0, 1)
        v3 = __index_by_global_array(seed_idx)
    elif v3 >= 0x4E0: # Array 3
        __heavy_xor_complex(seed_idx + 0x271, 0xE3, 0x18D, 1, 2, -0x270, 0, 1)
        __heavy_xor_complex(seed_idx + 0x354, 0x18C, -0x353, 1, 2, -0x270, 0, 1)
        __heavy_xor_complex(seed_idx, 1, 0x18D, 1, 2, 0x270, 0x4E0, 1)
        v3 = 0
        __store_global_array(seed_idx, 0)

    v14 = __index_by_global_array(seed_idx + v3 + 1)
    __store_global_array(seed_idx, v3 + 1)

    _4e1 = __index_by_global_array(seed_idx + 0x4E1)

    temp1 = (v14 >> 0xB) & _4e1 ^ v14
    temp2 = (temp1 & 0xFF3A58AD) << 7
    temp2 &= 0xFFFFFFFF

    v15 = temp2 ^ temp1

    temp4 = (((v15 & 0xFFFFDF8C) << 15) & 0xFFFFFFFF)
    temp5 = temp4 ^ v15

    ret = temp5 ^ (temp5 >> 0x12)
    return ret & 0xFFFFFFFF


def B16DA0_CreateRandomArray(seeds, size):
    elements_count = (size >> 2) & 0xFFFFFFFF # Elements count of some_memory, number of ints
    if not size:
        raise ValueError(f"Missing size!")

    random_seeds_length = len(seeds)
    
    if elements_count < 7:
        v6 = (elements_count - 1) >> 1
    elif elements_count < 0x27:
        v6 = 3
    elif elements_count < 0x44:
        v6 = 5
    elif elements_count < 0x26F:
        v6 = 7
    else:
        v6 = 11

    v7 = max(elements_count, random_seeds_length + 1)
    v8 = (elements_count - v6) >> 1
    v9 = v32 = v8 + v6

    state_array = bytearray()
    for _ in range(elements_count):
        state_array.extend(struct.pack("<I", 0x8B8B8B8B))

    loop_counter = 0
    if (v7):
        while (loop_counter < v7):
            v13 = (loop_counter + v8) % elements_count
            v14 = index_by(state_array, v13)
            v15_idx = loop_counter % elements_count
            v15 = index_by(state_array, v15_idx)
            temp = index_by(state_array, (loop_counter - 1) % elements_count)
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
            store_at_index(state_array, v13, (v14 + v16) & 0xFFFFFFFF)
            v19 = loop_counter + v32
            v19 &= 0xFFFFFFFF
            loop_counter += 1
            loop_counter &= 0xFFFFFFFF
            store_val = index_by(state_array, v19 % elements_count) + v18
            store_val &= 0xFFFFFFFF
            store_at_index(state_array, v19 % elements_count, store_val)
            store_at_index(state_array, v15_idx, v18)

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
            v25 = index_by(state_array, v24)
            v26_idx = v24
            v27 = (v21 + 1) & 0xFFFFFFFF
            v27 %= elements_count
            temp1 = index_by(state_array, v27)
            temp2 = index_by(state_array, v21 % elements_count)
            temp_val = v25 + temp1 + temp2
            temp_val &= 0xFFFFFFFF
            v28 = 0x5D588B65 * (temp_val ^ (temp_val >> 27))
            v28 &= 0xFFFFFFFF
            v29 = (v23 + v21) & 0xFFFFFFFF
            v29 %= elements_count
            v30 = v21 + 2
            v21 += 1
            store_at_index(state_array, v26_idx, v28 ^ v25)
            store_at_index(state_array, v29, index_by(state_array, v29) ^ ((v28 - v27) & 0xFFFFFFFF))
            store_at_index(state_array, v27, (v28 - v27) & 0xFFFFFFFF)

    return state_array


def validate_memories(xor_loc: int, arr1_loc: int = 0x1431FB5BC):
    compare_memory(GLOBAL_ARRAY[3], arr1_loc)
    compare_memory(GLOBAL_ARRAY[4], arr1_loc + (0x9C0-4))
    # compare_memory(GLOBAL_ARRAY[7][5], xor_loc)
    with open("xors.bin", "rb") as f:
        xors = bytearray(f.read())
        compare_bytearrays(GLOBAL_ARRAY[7][5], xors)


GLOBAL_ARRAY = [ # Replace with a bytes array
    0x00000000,  # 0x00
    0x00000270,  # 0x04
    0x00001571,  # 0x08 # This is actually an array of size 0x9C0 with the one on the bottom, but the first element needs to be seeded
    bytearray(0x9BC),  # 0x0C # Size 0x9BC
    bytearray(0x9C0),  # 0x9C0 # Size 0x9C8 # This is actually another array of size 0x9C0
    -1 & 0xFFFFFFFF, # From EXE
    0,
    "ptr_to_vr2_seed_array",
]
if __name__ == "__main__":
    initialize_state(GLOBAL_ARRAY[2])
    recreate_seed_array_1()

    validate_memories(0xD9D4CE0)

    # Get seeds for hash
    # for seed in [
    #     1231849, 1510674, 367050, 847834,
    # ]:
    #     print("Seed", seed)

    #     val = index_by(GLOBAL_ARRAY[7][5], seed, 1)
    #     val2 = index_by(GLOBAL_ARRAY[7][5], seed+4, 1)
    #     print()
    #     print(f"{seed}: {val},")
    #     print(f"{seed+4}: {val2},")
    #     print(hex(val ^ val2))
