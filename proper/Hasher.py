import struct


class VR2Hasher:
    PAD_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    CONST_31FA274 = 0xA7AC5CC0
    CONST_31FA270 = 3
    DEFAULT_SEED = 0x291

    def __init__(self, key_1: int, key_2: int, key_3: int, key_4: int, seed: int = DEFAULT_SEED):
        self.keys = [
            key_1, key_2, key_3, key_4
        ]
        self.seed = seed

    @classmethod
    def ROL4(cls, value, shift):
        value &= 0xFFFFFFFF
        l = (value << shift) & 0xFFFFFFFF
        r = (value >> (32 - shift)) & 0xFFFFFFFF
        return l | r

    @classmethod
    def ROL_XOR4(cls, value, shift):
        value &= 0xFFFFFFFF
        l = (value << shift) & 0xFFFFFFFF
        r = (value >> shift) & 0xFFFFFFFF
        return l ^ r

    @classmethod
    def uint32_from_bytes(cls, bytearray, offset):
        val = struct.unpack_from("<I", bytearray, offset)[0]
        return val

    @classmethod
    def resign_seeds(cls, *seeds: int):
        inputs = [a & 0xFFFFFFFF for a in seeds]
        return inputs

    @classmethod
    def magic_division(cls, value, magic, extra_shift=0):
        # Multiply, keep the high 64 bits, then shift, then sign-correct.
        prod = value * magic
        hi = prod >> 64
        return (hi >> extra_shift) + (hi >> 63)

    @classmethod
    def pad_string(cls, string: str, pad_length: int = 12) -> str:
        if len(string) % pad_length != 0:
            return string + cls.PAD_ALPHA[: pad_length - (len(string) % pad_length)]

        return string

    @property
    def ADE9B0(self):
        # self.CONST_31FA274
        return self.CONST_31FA270

    def B1CFA0(self, seed2_copy: int, seed2: int, seed3: int, seed1: int, seed4: int):
        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if seed2_copy <= 0:
            return seed1, seed2, seed3, seed4

        seed2 -= seed3
        seed2 &= 0xFFFFFFFF
        seed1 ^= 0x200

        v9 = seed1 + seed3
        v9 &= 0xFFFFFFFF
        seed1 = v9
        seed1 &= 0xFFFFFFFF
        seed2 -= v9
        seed2 &= 0xFFFFFFFF
        seed3 ^= 0x199
        seed3 &= 0xFFFFFFFF
        seed3 += seed1
        seed3 &= 0xFFFFFFFF
        seed4 -= 3
        seed4 &= 0xFFFFFFFF

        if (seed2_copy % 678) > 31:
            seed1, seed2, seed3, seed4 = self.B1D4C0(
                seed2_copy // self.ADE9B0 - 3, seed2, seed3, seed1, seed4
            )

        if (seed2_copy % 7) < 3:
            division_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.B1D120(
                division_result - 6, seed2, seed3, seed1, seed4
            )

        if (seed2_copy % 11) > 4:
            seed1, seed2, seed3, seed4 = self.B1D280(
                seed2_copy // 7 - 6, seed2, seed3, seed1, seed4
            )

        return seed1, seed2, seed3, seed4

    def B1D4C0(self, seed2_copy, seed2, seed3, seed1, seed4):
        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if seed2_copy <= 0:
            return seed1, seed2, seed3, seed4

        seed3 -= seed2
        seed3 &= 0xFFFFFFFF
        v9 = self.ROL4(seed2, 3)
        seed3 ^= v9
        seed2 += seed1
        seed2 &= 0xFFFFFFFF
        seed1 -= seed3
        seed1 &= 0xFFFFFFFF
        v10 = self.ROL4(seed3, 2)
        seed2 ^= v10
        seed3 += seed1
        seed3 &= 0xFFFFFFFF
        seed4 += 9
        seed4 &= 0xFFFFFFFF
        seed2 ^= seed4

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if seed2_copy % 4 == 0:
            division_result = self.magic_division(seed2_copy, 0x4924924924924925, 1)
            seed1, seed2, seed3, seed4 = self.B1CFA0(division_result - 3, seed2, seed3, seed1, seed4)

        if (seed2_copy % 5) < 3:
            div_result = seed2_copy // 4
            seed1, seed2, seed3, seed4 = self.B1D120(div_result - 6, seed2, seed3, seed1, seed4)

        if (seed2_copy % 8) > 4:
            div_result = self.magic_division(seed2_copy, 0x5555555555555556)
            seed1, seed2, seed3, seed4 = self.B1D280(div_result - 6, seed2, seed3, seed1, seed4)

        return seed1, seed2, seed3, seed4

    def B1D120(self, seed2_copy, seed2, seed3, seed1, seed4):
        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if seed2_copy <= 0:
            return seed1, seed2, seed3, seed4

        seed2 -= seed3
        seed2 &= 0xFFFFFFFF
        seed1 ^= (seed3 << 7) ^ ((seed3 & 0xFFFFFFFF) >> 7)
        seed1 += seed3
        seed1 &= 0xFFFFFFFF
        seed4 *= 5
        seed4 &= 0xFFFFFFFF

        if (seed2_copy & 1) == 0:
            div_result = self.magic_division(seed2_copy, 0x5555555555555556)
            seed1, seed2, seed3, seed4 = self.B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
        if (seed2_copy % 7) < 3:
            div_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
        if (seed2_copy % 11) > 4:
            div_result = seed2_copy // 7
            seed1, seed2, seed3, seed4 = self.B1D280(div_result - 6, seed2, seed3, seed1, seed4)

        return seed1, seed2, seed3, seed4

    def B1D280(self, seed2_copy, seed2, seed3, seed1, seed4):  # REMADE
        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if seed2_copy <= 0:
            return seed1, seed2, seed3, seed4

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF
        v9 = self.ROL4(seed1, 2)
        seed2 ^= v9
        seed2 += seed3
        seed2 &= 0xFFFFFFFF
        seed4 *= 8
        seed4 &= 0xFFFFFFFF
        seed2 ^= seed4

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        if (seed2_copy % 7) > 3:
            div_result = self.magic_division(seed2_copy, 0x4924924924924925, 2)
            seed1, seed2, seed3, seed4 = self.B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
        if (seed2_copy % 9) < 2:
            div_result = self.magic_division(seed2_copy, 0x5555555555555556)
            seed1, seed2, seed3, seed4 = self.B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
        if (seed2_copy % 131) > 66:  # USED
            div_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.B1D280(div_result - 7, seed2, seed3, seed1, seed4)

        return seed1, seed2, seed3, seed4

    def hash_step_0(self, seed1: int, seed3: int, seed2: int, seed4: int, v120: int):
        seed3_ptr2 = seed3

        seed1 += seed3_ptr2
        seed1 &= 0xFFFFFFFF

        seed2_ptr2 = seed2

        seed3 -= seed2_ptr2
        seed3 &= 0xFFFFFFFF

        v8 = self.ROL4(seed2, 2)
        seed3 ^= v8

        v12 = seed1

        seed2 += v12
        seed2 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self.B1CFA0(seed2, seed2, seed3, seed1, seed4)

        v15 = self.keys[2]

        seed2 ^= v15

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF

        v19 = self.ROL4(seed1, 14)

        seed2 ^= v19

        seed1 += seed3
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        return seed1, seed2, seed3, seed4, v120

    def hash_step_80(self, v48: int, seed3: int, seed1: int, seed2: int, v120: int, seed4: int):
        v48 = self.ROL4(seed3, 4)
        if seed1 > seed3:
            seed1, seed2, seed3, v48, v120 = self.hash_step_80_internal(seed1, seed3, v48, seed2, v120)

        v3 = self.keys[0]

        seed1 ^= v3
        seed1 += 1
        seed1 &= 0xFFFFFFFF
        seed4 = seed3

        seed3, seed1, seed2, seed4 = self.B1D4C0(seed1, seed1, seed2, seed3, seed4)

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF
        v12 = self.ROL4(seed1, 13)

        seed2 ^= v12

        seed1 += seed3
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)
        return seed1, seed2, seed3, seed4, v120, v48

    def hash_step_60(self, seed3: int, seed2: int, seed1: int, seed4: int, v120: int):
        seed3 -= seed2
        seed3 &= 0xFFFFFFFF
        
        v5 = self.ROL_XOR4(seed2, 5) 
        seed1 ^= v5

        seed2 += seed3
        seed2 &= 0xFFFFFFFF

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF
        v13 = self.ROL4(seed1, 6)
        seed2 ^= v13
        seed1 += seed3
        seed1 &= 0xFFFFFFFF
        seed1 -= seed3
        seed1 &= 0xFFFFFFFF
        v21 = self.ROL4(seed3, 16)
        seed1 ^= v21
        seed3 += seed2
        seed3 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)

        seed1, seed3, seed2, seed4 = self.B1D120(seed3, seed3, seed2, seed1, seed4)

        v28 = self.keys[3]
        seed3 ^= v28
        seed3 -= seed2
        seed3 &= 0xFFFFFFFF
        v32 = self.ROL4(seed2, 3)
        seed3 ^= v32
        seed2 += seed1
        seed2 &= 0xFFFFFFFF
        seed3 -= seed2
        seed3 &= 0xFFFFFFFF
        v40 = self.ROL4(seed2, 4)
        seed3 ^= v40
        seed2 += seed1
        seed2 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self.resign_seeds(seed1, seed2, seed3, seed4)
        return seed1, seed2, seed3, seed4, v120

    def hash_step_20(self, seed3: int, seed2: int, seed1: int, v120: int):
        seed3 -= seed2
        seed3 &= 0xFFFFFFFF
        v5 = self.ROL4(seed2, 8)
        seed3 ^= v5
        seed2 += seed1
        seed2 &= 0xFFFFFFFF
        seed2 -= seed1
        seed2 &= 0xFFFFFFFF
        v13 = self.ROL4(seed1, 11)
        seed2 ^= v13

        seed1, seed2, seed3 = self.resign_seeds(seed1, seed2, seed3)
        return seed1, seed2, seed3, v120

    def hash_step_40(self, seed2: int, seed3: int, seed1: int, v120: int):
        v4 = self.keys[1]
        seed2 ^= v4
        seed2 -= seed3
        seed2 &= 0xFFFFFFFF
        v8 = self.ROL4(seed3, 12)
        seed2 ^= v8
        seed1 += seed2
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3 = self.resign_seeds(seed1, seed2, seed3)

        return seed1, seed2, seed3, v120

    def hash_step_80_internal(self, seed1: int, seed3: int, v48: int, seed2: int, v120: int):
        seed1 -= seed3
        seed1 &= 0xFFFFFFFF
        seed1 ^= v48
        seed3 += seed2
        seed3 &= 0xFFFFFFFF

        seed1, seed2, seed3, v48 = self.resign_seeds(seed1, seed2, seed3, v48)

        return seed1, seed2, seed3, v48, v120

    def vr2_inner_hash(self, active_thread_id: int, seed1: int, seed2: int, seed3: int, seed4: int):
        v120 = 3
        v48 = 0

        if active_thread_id == 0:
            seed1, seed2, seed3, seed4, v120 = self.hash_step_0(seed1, seed3, seed2, seed4, v120)
            next_thread_id = 60
        elif active_thread_id == 20:
            seed1, seed2, seed3, v120 = self.hash_step_20(seed3, seed2, seed1, v120)
            next_thread_id = 0
        elif active_thread_id == 40:
            seed1, seed2, seed3, v120 = self.hash_step_40(seed2, seed3, seed1, v120)
            next_thread_id = 20
        elif active_thread_id == 60:
            seed1, seed2, seed3, seed4, v120 = self.hash_step_60(seed3, seed2, seed1, seed4, v120)
            next_thread_id = 20
        elif active_thread_id == 80:
            seed1, seed2, seed3, seed4, v120, v48 = self.hash_step_80(v48, seed3, seed1, seed2, v120, seed4)
            next_thread_id = 40
        else:
            raise ValueError(f"Incorrect Thread Id passed! {active_thread_id}")

        return next_thread_id, seed1, seed2, seed3, seed4

    def vr2_hash(self, string: bytes, seed: int):
        string_length = len(string)

        seed3_v74 = seed_4v44 = total_read_string_bytes = 0
        v9 = ((seed - 1) | 0x80000000) + (4 * string_length)
        seed3_v74 = v10 = seed2_v41 = v11 = seed1_v40 = v9

        if string_length < 0x0C:
            return seed3_v74

        string_seeder_offset = 8

        while True:
            seed2_v41 = self.uint32_from_bytes(string, string_seeder_offset - 4) + v10
            seed2_v41 &= 0xFFFFFFFF

            v14 = self.uint32_from_bytes(string, string_seeder_offset) + v9
            v14 &= 0xFFFFFFFF

            temp = v14 << 4
            temp &= 0xFFFFFFFF  # Enforce 32b

            temp2 = v14 >> 28

            left_side = temp2 | temp
            left_side &= 0xFFFFFFFF

            right_side = self.uint32_from_bytes(string, total_read_string_bytes) + v11 - v14
            right_side &= 0xFFFFFFFF

            seed1_v40 = left_side ^ right_side

            seed3_v74 = (seed2_v41 + v14) & 0xFFFFFFFF

            active_thread_id = 80  # 0x50

            for _ in range(5):
                active_thread_id, seed1_v40, seed2_v41, seed3_v74, seed_4v44 = self.vr2_inner_hash(active_thread_id, seed1_v40, seed2_v41, seed3_v74, seed_4v44)

            string_seeder_offset += 12
            total_read_string_bytes += 12

            if string_seeder_offset + 4 <= string_length:
                v11 = seed1_v40
                v10 = seed2_v41
                v9 = seed3_v74
                continue

            break

        return seed3_v74

    def hash(self, string: str):           
        padded = self.pad_string(string).encode("ascii")
        hashed = self.vr2_hash(padded, self.seed)
        return hex(hashed)

if __name__ == "__main__":
    keys = [0x7df1d6dc, 0xbd3e1588, 0x86e2354d, 0xeaa35755]
    hasher = VR2Hasher(*keys)
    hash = hasher.hash("test23")
    print(hash)
