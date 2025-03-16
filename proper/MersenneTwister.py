from datetime import datetime
import struct
from typing import List

import numpy as np


def dump(*arrays, name: str):
    if not name.lower().endswith(".bin"):
        name += ".bin"
    array = bytearray()
    for a in arrays:
        array += a
    with open(name, "wb") as f:
        f.write(array)


def str_to_bytes(bytearray, offset):
    val = struct.unpack_from("<I", bytearray, offset)[0]
    return val

def index_by(bytearray, index, size: int = 4):
    val = str_to_bytes(bytearray, index * size)
    return val

def store_at_index(bytearray, index, value, size: int = 4):
    struct.pack_into("<I", bytearray, index * size, value)

def get_bitmask_ff(size: int):
    # Create a bitmask based on size (e.g., 0xFF for 1 byte, 0xFFFF for 2 bytes, etc.)
    return (1 << (size * 8)) - 1

def resign_seeds(*seeds: int, size: int = 4):
    mask = get_bitmask_ff(size)
    inputs = [a & mask for a in seeds]
    return inputs


class MT19937:
    n = 624  # 0x270
    m = 397  # 0x18D
    w = 32
    r = 31
    a = 0x9908B0DF
    u = 11
    d = -1 & 0xFFFFFFFF
    s = 7
    t = 15
    l = 18
    f = 1812433253

    DEFAULT_SEED = 0x1571

    def __init__(self):
        self.init = False
        self.state_index = 0
        self.xor_key = 0
        self.xor_consts = [0]*4
        self.xor_array = bytearray()

    def initialize_state(self, seed: int = DEFAULT_SEED):
        result_arr = bytearray()
        for i in range(1, self.n):
            seed = ((self.f * (seed ^ (seed >> (self.w-2)))) & 0xFFFFFFFF) + i
            seed &= 0xFFFFFFFF
            result_arr.extend(struct.pack("<I", seed))

        self.state_array = result_arr
        self.state_index = self.n
        self.temp_state_array = bytearray(self.n*4)

    def create_randoms_array(self, seeds: List[int]):
        size = self.n * 4
        elements_count = size >> 2 # Elements count of some_memory, number of ints
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
        v9 = v8 + v6

        state_array = bytearray()
        for _ in range(elements_count):
            state_array.extend(struct.pack("<I", 0x8B8B8B8B))

        for loop_counter in range(v7):
            v13 = (loop_counter + v8) % elements_count
            v14 = index_by(state_array, v13)
            v15_idx = loop_counter % elements_count
            v15 = index_by(state_array, v15_idx)
            temp = index_by(state_array, (loop_counter - 1) % elements_count)
            v16 = 0x19660D * (v15 ^ v14 ^ temp ^ ((v15 ^ v14 ^ temp) >> 27))
            v16 &= 0xFFFFFFFF
            if loop_counter == 0:
                v17 = random_seeds_length
            elif loop_counter > random_seeds_length:
                v17 = loop_counter % elements_count
            else:
                idx = (loop_counter-1)%random_seeds_length
                v17 = loop_counter % elements_count + seeds[idx]
                v17 &= 0xFFFFFFFF

            v18 = v17 + v16
            v18 &= 0xFFFFFFFF
            store_at_index(state_array, v13, (v14 + v16) & 0xFFFFFFFF)

            v19 = (loop_counter + v9) % elements_count
            v19 &= 0xFFFFFFFF

            store_val = index_by(state_array, v19) + v18
            store_val &= 0xFFFFFFFF
            store_at_index(state_array, v19, store_val)
            store_at_index(state_array, v15_idx, v18)

        v21, v22, v23 = resign_seeds(v7 - 1, v8 + 1, v9 + 1)

        for _ in range(v7, elements_count + v7):
            v24 = (v22 + v21) % elements_count
            v25 = index_by(state_array, v24)
            v27 = (v21 + 1) % elements_count

            temp1 = index_by(state_array, v27)
            temp2 = index_by(state_array, v21 % elements_count)
            temp_val = (v25 + temp1 + temp2) & 0xFFFFFFFF

            v28 = (0x5D588B65 * (temp_val ^ (temp_val >> 27))) & 0xFFFFFFFF
            v29 = (v23 + v21) % elements_count

            store_at_index(state_array, v24, v28 ^ v25)
            store_at_index(
                state_array, v29, index_by(state_array, v29) ^ ((v28 - v27) & 0xFFFFFFFF)
            )
            store_at_index(state_array, v27, (v28 - v27) & 0xFFFFFFFF)

            v21 += 1

        return state_array

    def store_xor_const(self, result_index, initial_value, next_index, next_index_2):
        # Fancy function that just stores XOR values in order
        v7 = next_index  # index to compare against
        v8 = v7 + 1  # index 1
        v9 = next_index_2
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
            raise ValueError(
                f"v13 was 0. Something went wrong! (Will cause infinite recursion)"
            )
        if v13 < 0x1000:
            pass  # Do nothing since it should go fine # The pass is there so I can track it in ida if I need
            # v16 = [[]] * v11 # Array of size 4 # Not needed since I can directly modify my memory
        else:
            raise NotImplementedError(
                f"This area is not tested! Erroring so you can trace!"
            )

        self.xor_consts[result_index] = initial_value
        return v8, v12 // 4

    def _generate_random_seeds(self, n: int = 8):
        if n < 1:
            raise ValueError(f"Expecting at least 1 n")

        factor = 1e-7
        seed_1 = 0x41987E9DB71 # Unsure how to create, research later
        time_factor = seed_1 * factor
        ts = int(datetime.now().timestamp()) & 0xFFFFFFFF
        ts *= time_factor 
        ts = int(ts) & 0xFFFFFFFF

        seeds = [ts]
        for i in range(len(seeds), n):
            rand_bytes = np.random.bytes(4)
            rand_int = int.from_bytes(rand_bytes, byteorder="little", signed=False)
            seeds.append(rand_int)

        return seeds

    def create_xor_arrays(self, array_size: int, element_size: int = 4):
        if array_size % 16 or array_size < 100_000 or element_size > 20:
            raise ValueError(f"Incorrect XOR Array Config!")

        array_elements_count = array_size >> 2
        xor_array = bytearray(array_size)
        for v10 in range(array_elements_count):
            store_at_index(xor_array, v10, self.twist())

        next_xor_index = next_xor_index_2 = 0
        self.xor_key = 0

        v12 = 0
        if self.unsigned_to_signed(element_size) >= 0:
            v14 = (array_size // element_size - 20) >> 1
            v15 = array_size - 20
            for v13 in range(element_size):
                v27 = self.twist()
                v12 += v14 + v27 % v14 + 0x14
                # v67 = v12

                if v12 > v15:
                    return

                # v28 = next_xor_index
                # if next_xor_index_2 == next_xor_index:
                # next_xor_index, next_xor_index_2 = self.store_xor_const(v28, v67, next_xor_index, next_xor_index_2)
                #     v12 = v67
                # else:
                #     v28 = v12
                #     next_xor_index_2 += 1
                self.xor_consts[v13] = v12

        v29 = 4 * element_size
        v29 &= 0xFFFFFFFF
        if self.unsigned_to_signed(v29) <= 0:
            return

        for _ in range(v29):
            v43 = self.twist() % element_size
            v55 = self.twist() % element_size
            if v43 != v55:
                v56 = self.xor_consts[v55]
                v57 = self.xor_consts[v43]

                self.xor_consts[v55] = v57
                self.xor_consts[v43] = v56

        v59 = self.twist()
        self.xor_key = v59
        s_size = self.unsigned_to_signed(element_size)
        if s_size > 0 and element_size >= 0x10:
            raise NotImplementedError(f"Element Size >= 10 is not supported")

        for i in range(element_size):
            self.xor_consts[i] ^= self.xor_key

        return xor_array

    def twist(self):
        if self.state_index == self.n:
            self.complex_xor(self.n, 0, self.m, self.n)
        elif self.state_index >= self.n*2:  # Array 3
            self.complex_xor(self.n - self.m, self.n, self.m, -self.n)
            self.complex_xor(self.m - 1, self.n * 2 - self.m, -(self.n * 2 - self.m), -self.n)
            self.complex_xor(1, self.n * 2 - 1, self.m, self.n, allow_overflow=True)
            self.state_index = 0

        v14 = self.get_state_idx(self.state_index)
        self.state_index += 1

        temp1 = (v14 >> self.u) & self.d ^ v14
        temp2 = (temp1 & 0xFF3A58AD) << self.s
        temp2 &= 0xFFFFFFFF

        v15 = temp2 ^ temp1

        temp4 = ((v15 & 0xFFFFDF8C) << self.t) & 0xFFFFFFFF
        temp5 = temp4 ^ v15

        ret = temp5 ^ (temp5 >> self.l)
        return ret & 0xFFFFFFFF

    def create_state_array(self, seeds: List[int] = [], amount: int = 2_000_000):
        seeds = seeds[:8]
        if len(seeds) < 8:
            seeds = self._generate_random_seeds(8)

        self.init = True

        self.state_array = self.create_randoms_array(seeds)
        v7 = 0
        for v8 in range(self.n):
            v7 |= index_by(self.state_array, v8)

        if v7 < 0x80000000:
            raise ValueError(f"v7 < 0x80000000")

        self.state_index = self.n
        self.xor_array = self.create_xor_arrays(amount)

    def get_state_idx(self, state_idx: int):
        if state_idx >= self.n * 2:
            raise IndexError(f"Maximum index size is {self.n*2}")

        if state_idx < self.n:
            return index_by(self.state_array, state_idx)

        return index_by(self.temp_state_array, state_idx - self.n)

    def set_at_state_idx(self, state_idx: int, value):
        if state_idx >= self.n * 2:
            raise IndexError(f"Maximum index size is {self.n*2}")

        if state_idx < self.n:
            return store_at_index(self.state_array, state_idx, value)

        return store_at_index(self.temp_state_array, state_idx - self.n, value)

    def derive_new_keys_from_string(self, encryption_string: bytes):
        """
        Short implementation of MK11.exe+B1AD50
        """
        v3 = b""
        v4 = 0
        v5 = len(encryption_string)
        v6 = 0
        if v5:
            v7 = v5 - 1
            if v5 - 1 > 0x28:
                if v5 - 0x17 >= 0:
                    v9 = -1
                    if v5 - 0x17 < v7:
                        v9 = -23
                    v8 = v5 + v9
                else:
                    v8 = 0
                v10 = v7 - v8
                if v10 > 12:
                    v10 = 12
                v11 = 0  # index into encryption string
                v4 = v10 + 1
                if not v10:
                    v4 = 0
                v6 = v4
                v3 = b""
                if v4:
                    v3 = encryption_string[
                        v11 + v8 + 1 : v11 + v8 + v10 + 1
                    ]  # Copy specific bytes from
                v12 = v3
                if not v4:
                    v12 = b""  # Null
            else:
                v12 = b""
        else:
            v12 = b""

        v16 = self._key_seed_from_str(v12, 0, 0x9FD33AE8, 0x1169237E, 0x70263B48, 0x9FD33A, 0x11, 0x1169)

        v17 = b""
        if v6:
            v17 = v3
        v44 = self._key_seed_from_str(v17, 1, 0x3B9FA118, 3756927701, -0x7720C8E, 0x3B9FA1, 0x11, 0xDFEE)

        v21 = b""
        if v4:
            v21 = v3
        v25 = self._key_seed_from_str(v21, 2, -538039595, 0xE7026B48, 0x9C1BF55D, 0xDFEE2A, 17, 0xE702)

        v26 = b""
        if v4:
            v26 = v3

        v30 = self._key_seed_from_str(v26, 3, -0x18FD94B8, 0xDFEE2AD5, 0x29C08DAF, 0xE7026B, 0x11, 0xDFEE)

        v31 = v16 ^ v44
        v32 = v25 ^ v44
        v33 = v25 ^ v30
        v45 = v31 ^ v30

        key_1 = v31 ^ 0x77E56F3D
        key_2 = v32 ^ 0x250A0D57
        key_3 = v33 ^ 0xA4CA9627
        key_4 = v45 ^ 0x9414718A

        new_keys = [
            key_1, key_2, key_3, key_4
        ]

        for i, n_k in enumerate(new_keys):
            index = self.xor_key ^ self.xor_consts[i]
            r_val = index_by(self.xor_array, index + 4, 1)
            store_at_index(self.xor_array, index, r_val ^ n_k, 1)

    def get_keys(self):
        keys = []
        for key in self.xor_consts:
            index = key ^ self.xor_key
            left  = index_by(self.xor_array, index, 1)
            right = index_by(self.xor_array, index+4, 1)
            keys.append(left ^ right)
        return keys

    def complex_xor(self, range_: int, index_offset: int, xor_offset: int, store_offset: int, allow_overflow: bool = False):
        for _ in range(range_):
            next = (index_offset + 1)
            next_xor = (index_offset + xor_offset)
            next_store = (index_offset + store_offset)
            if allow_overflow:
                next %= (self.n*2)
                next_xor %= (self.n*2)
                next_store %= (self.n*2)
                index_offset %= self.n*2

            idx_1 = self.get_state_idx(index_offset)
            idx_2 = self.get_state_idx(next)
            idx_xor = self.get_state_idx(next_xor) # handle if xor > or < and see where to get it from
            temp_xor = idx_1 ^ idx_2
            store_val_l = ((idx_1 ^ temp_xor & 0x7FFFFFFF) >> 1) ^ idx_xor
            store_val_r = 0
            if idx_2 & 1 != 0:
                store_val_r = 0x9908B0DF

            self.set_at_state_idx(next_store, store_val_l ^ store_val_r)
            index_offset += 1

    @classmethod
    def _key_seed_from_str(cls, string, offset, mul_2, mul_1, mul_3, add_2, add_3, add_1):
        v13 = string[8 + offset]
        v14 = string[4 + offset]
        v15 = string[offset]

        v1 = mul_2 * v14
        v1 &= 0xFFFFFFFF

        v2 = mul_1 * v13
        v2 &= 0xFFFFFFFF

        v3 = mul_3 * v15
        v3 &= 0xFFFFFFFF

        v4 = v14 + add_2
        v4 &= 0xFFFFFFFF

        v5 = v15 + add_3
        v5 &= 0xFFFFFFFF

        v6 = v13 + add_1
        v6 &= 0xFFFFFFFF

        mul = v4 * v5
        mul &= 0xFFFFFFFF
        mul *= v6
        mul &= 0xFFFFFFFF
        val = v1 + v2 + v3 + mul

        return val & 0xFFFFFFFF

    def unsigned_to_signed(self, value: int, mask_size: int = 4):
        mask = (1 << (mask_size * 8)) - 1  # Ensure value stays within 32-bit
        value &= mask
        limit = 1 << (mask_size * 8 - 1)  # 0x80000000 (sign bit)

        if value >= limit:  # If the value is in the negative range
            return value - (1 << (mask_size * 8))  # Convert to signed

        return value  # Return as is if positive


if __name__ == "__main__":

    seed = 0x1571

    print("Initializing MT19937 with seed", seed)
    rng = MT19937()
    rng.initialize_state(seed)
    print("Creating randoms")
    rng.create_state_array(
        [
            0x84AC2951,
            0xC921BAD3,
            0x629F23FB,
            0x21A1E46F,
            0xFB9B121F,
            0x26366388,
            0x8BB37CD1,
            0x6A1858D5,
        ]
    )

    print("Results")
    print(rng.xor_consts)
    print([hex(a) for a in rng.xor_consts])
    print(rng.get_keys())
    print([hex(a) for a in rng.get_keys()])

    print("Reseed!")
    rng.derive_new_keys_from_string(string)
    print(rng.get_keys())
    print([hex(a) for a in rng.get_keys()])
