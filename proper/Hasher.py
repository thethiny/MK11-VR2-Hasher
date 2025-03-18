import struct
from typing import Any, List, Optional, Tuple, Union, overload

from proper.MersenneTwister import MT19937
from utils import index_by, store_at_index


class VR2Hasher:
    PAD_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    CONST_31FA274 = 0xA7AC5CC0
    CONST_31FA270 = 3
    DEFAULT_SEED = 0x291

    def __init__(
        self,
        hash_seed: int = DEFAULT_SEED,
        calculate_randoms: bool = False,
        mt_seed: Optional[int] = None,
        mt_seed_array: List[int] = [],
        encryption_string: Union[str, bytes] = "",
        xor_array_size: int = 2_000_000,
        vr2_keys: List[int] = [],
    ):
        self._seed = hash_seed
        self._mt_seed = 0
        self.__mt_init = False
        self.__init = False

        self._keys = []
        self._xor_key = 0
        self._xor_consts = [0]*4
        self._xor_array = bytearray()
        
        if vr2_keys:
            if len(vr2_keys) != 4:
                raise ValueError(f"In order to override the VR2 Keys you need to pass 4 keys.")
            
            self._keys = vr2_keys
            self.__init = True
            return

        if encryption_string and isinstance(encryption_string, str):
            encryption_string = encryption_string.encode("ascii")

        if calculate_randoms:
            self.__mt_init = True
            self._mt_seed = mt_seed or MT19937.DEFAULT_SEED
            self._mt = MT19937()
            self._mt.initialize_state(self._mt_seed)
            self._mt.create_state_array(mt_seed_array)
            self.__mt_init = True

            self._xor_array = self.create_xor_arrays(array_size=xor_array_size, element_size=4)

            if encryption_string:
                new_keys = self.derive_new_keys_from_string(encryption_string)
                self.set_keys(new_keys)

            self._keys = self.get_keys()

        elif encryption_string:
            if isinstance(encryption_string, str):
                encryption_string = encryption_string.encode("ascii")
            self._keys = self.derive_new_keys_from_string(encryption_string)
        else:
            raise ValueError(f"Either `calculate_randoms` must be set, or `encryption_string` must be provided!")

        self.__init = True

    @property
    def keys(self):
        if not self.__init:
            raise ValueError(f"VR2 Hasher is not yet initialized!")
        return self._keys

    @property
    def xor_key(self):
        if not self.__mt_init:
            if self.__init:
                raise ValueError("Cannot use 'xor_key' in shortcut mode as it is not calculated!")
            raise ValueError("VR2 Hasher is not yet initialized!")
        return self._xor_key

    @property
    def xor_consts(self):
        if not self.__mt_init:
            if self.__init:
                raise ValueError("Cannot use 'xor_consts' in shortcut mode as they are not calculated!")
            raise ValueError("VR2 Hasher is not yet initialized!")
        return self._xor_consts

    @property
    def xor_array(self):
        if not self.__mt_init:
            if self.__init:
                raise ValueError("Cannot use 'xor_array' in shortcut mode as it is not calculated!")
            raise ValueError("VR2 Hasher is not yet initialized!")
        return self._xor_array

    @property
    def mt(self):
        if not self.__mt_init:
            if self.__init:
                raise ValueError("Cannot use 'mt' in shortcut mode as it is not initialized!")
            raise ValueError("VR2 Hasher is not yet initialized!")
        return self._mt

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
    def _to_uint32(cls, *seeds: int):
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

    @classmethod
    def _key_seed_from_str(
        cls, string, offset, mul_2, mul_1, mul_3, add_2, add_3, add_1
    ):
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

    def create_xor_arrays(self, array_size: int, element_size: int = 4):
        if array_size % 16 or array_size < 100_000 or element_size > 20:
            raise ValueError(f"Incorrect XOR Array Config!")

        array_elements_count = array_size >> 2
        xor_array = bytearray(array_size)
        for v10 in range(array_elements_count):
            store_at_index(xor_array, v10, self._mt.random())

        self._xor_key = 0

        v12 = 0
        if self.unsigned_to_signed(element_size) >= 0:
            v14 = (array_size // element_size - 20) >> 1
            v15 = array_size - 20
            for v13 in range(element_size):
                v27 = self._mt.random()
                v12 += v14 + v27 % v14 + 0x14

                if v12 > v15:
                    return

                self._xor_consts[v13] = v12

        v29 = 4 * element_size
        v29 &= 0xFFFFFFFF
        if self.unsigned_to_signed(v29) <= 0:
            return

        for _ in range(v29):
            v43 = self._mt.random() % element_size
            v55 = self._mt.random() % element_size
            if v43 != v55:
                v56 = self._xor_consts[v55]
                v57 = self._xor_consts[v43]

                self._xor_consts[v55] = v57
                self._xor_consts[v43] = v56

        v59 = self._mt.random()
        self._xor_key = v59
        s_size = self.unsigned_to_signed(element_size)
        if s_size > 0 and element_size >= 0x10:
            raise NotImplementedError(f"Element Size >= 10 is not supported")

        for i in range(element_size):
            self._xor_consts[i] ^= self._xor_key

        return xor_array

    def derive_new_keys_from_string(self, encryption_string: bytes) -> List[int]:
        """
        Short implementation of MK11.exe+B1AD50
        encryption_string should be X-Hydra-Access-Token
        """
        if len(encryption_string) < 0x30:
            raise ValueError(f"Key must be at least 48 bytes")

        extracted_bytes = encryption_string[-22:-10]

        # Generate keys from extracted_bytes using _key_seed_from_str
        key_seed_1 = self._key_seed_from_str(extracted_bytes, 0, 0x9FD33AE8, 0x1169237E, 0x70263B48, 0x9FD33A, 0x11, 0x1169)
        key_seed_2 = self._key_seed_from_str(extracted_bytes, 1, 0x3B9FA118, 3756927701, -0x7720C8E, 0x3B9FA1, 0x11, 0xDFEE)
        key_seed_3 = self._key_seed_from_str(extracted_bytes, 2, -538039595, 0xE7026B48, 0x9C1BF55D, 0xDFEE2A, 17, 0xE702)
        key_seed_4 = self._key_seed_from_str(extracted_bytes, 3, -0x18FD94B8, 0xDFEE2AD5, 0x29C08DAF, 0xE7026B, 0x11, 0xDFEE)

        # Compute intermediate XOR operations
        xor_1 = key_seed_1 ^ key_seed_2
        xor_2 = key_seed_3 ^ key_seed_2
        xor_3 = key_seed_3 ^ key_seed_4
        xor_4 = xor_1 ^ key_seed_4

        # Compute final keys
        new_keys = [
            xor_1 ^ 0x77E56F3D,
            xor_2 ^ 0x250A0D57,
            xor_3 ^ 0xA4CA9627,
            xor_4 ^ 0x9414718A
        ]

        return new_keys

    def get_keys(self):
        if not self.__mt_init:
            return self.keys

        keys = []
        for key in self._xor_consts:
            index = key ^ self._xor_key
            left = index_by(self._xor_array, index, 1)
            right = index_by(self._xor_array, index + 4, 1)
            keys.append(left ^ right)
        return keys

    def set_keys(self, new_keys: List[int]):
        if len(new_keys) != 4:
            raise ValueError(f"Expecting 4 keys!")

        if not self.__mt_init:
            self._keys = new_keys
            return

        for i, key in enumerate(new_keys):
            index = self._xor_key ^ self._xor_consts[i]
            stored_value = index_by(self._xor_array, index + 4, 1)
            store_at_index(self._xor_array, index, stored_value ^ key, 1)

    def hash_round_B1CFA0(self, seed2_copy: int, seed2: int, seed3: int, seed1: int, seed4: int):
        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

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
            seed1, seed2, seed3, seed4 = self.hash_round_B1D4C0(
                seed2_copy // self.ADE9B0 - 3, seed2, seed3, seed1, seed4
            )

        if (seed2_copy % 7) < 3:
            division_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.hash_round_B1D120(
                division_result - 6, seed2, seed3, seed1, seed4
            )

        if (seed2_copy % 11) > 4:
            seed1, seed2, seed3, seed4 = self.hash_round_B1D280(
                seed2_copy // 7 - 6, seed2, seed3, seed1, seed4
            )

        return seed1, seed2, seed3, seed4

    def hash_round_B1D4C0(self, seed2_copy, seed2, seed3, seed1, seed4):
        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

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

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

        if seed2_copy % 4 == 0:
            division_result = self.magic_division(seed2_copy, 0x4924924924924925, 1)
            seed1, seed2, seed3, seed4 = self.hash_round_B1CFA0(division_result - 3, seed2, seed3, seed1, seed4)

        if (seed2_copy % 5) < 3:
            div_result = seed2_copy // 4
            seed1, seed2, seed3, seed4 = self.hash_round_B1D120(div_result - 6, seed2, seed3, seed1, seed4)

        if (seed2_copy % 8) > 4:
            div_result = self.magic_division(seed2_copy, 0x5555555555555556)
            seed1, seed2, seed3, seed4 = self.hash_round_B1D280(div_result - 6, seed2, seed3, seed1, seed4)

        return seed1, seed2, seed3, seed4

    def hash_round_B1D120(self, seed2_copy, seed2, seed3, seed1, seed4):
        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

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
            seed1, seed2, seed3, seed4 = self.hash_round_B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
        if (seed2_copy % 7) < 3:
            div_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.hash_round_B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
        if (seed2_copy % 11) > 4:
            div_result = seed2_copy // 7
            seed1, seed2, seed3, seed4 = self.hash_round_B1D280(div_result - 6, seed2, seed3, seed1, seed4)

        return seed1, seed2, seed3, seed4

    def hash_round_B1D280(self, seed2_copy, seed2, seed3, seed1, seed4):  # REMADE
        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

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

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

        if (seed2_copy % 7) > 3:
            div_result = self.magic_division(seed2_copy, 0x4924924924924925, 2)
            seed1, seed2, seed3, seed4 = self.hash_round_B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
        if (seed2_copy % 9) < 2:
            div_result = self.magic_division(seed2_copy, 0x5555555555555556)
            seed1, seed2, seed3, seed4 = self.hash_round_B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
        if (seed2_copy % 131) > 66:  # USED
            div_result = self.magic_division(seed2_copy, 0x6666666666666667, 1)
            seed1, seed2, seed3, seed4 = self.hash_round_B1D280(div_result - 7, seed2, seed3, seed1, seed4)

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

        seed1, seed2, seed3, seed4 = self.hash_round_B1CFA0(seed2, seed2, seed3, seed1, seed4)

        v15 = self._keys[2]

        seed2 ^= v15

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF

        v19 = self.ROL4(seed1, 14)

        seed2 ^= v19

        seed1 += seed3
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

        return seed1, seed2, seed3, seed4, v120

    def hash_step_80(self, v48: int, seed3: int, seed1: int, seed2: int, v120: int, seed4: int):
        v48 = self.ROL4(seed3, 4)
        if seed1 > seed3:
            seed1, seed2, seed3, v48, v120 = self.hash_step_80_internal(seed1, seed3, v48, seed2, v120)

        v3 = self._keys[0]

        seed1 ^= v3
        seed1 += 1
        seed1 &= 0xFFFFFFFF
        seed4 = seed3

        seed3, seed1, seed2, seed4 = self.hash_round_B1D4C0(seed1, seed1, seed2, seed3, seed4)

        seed2 -= seed1
        seed2 &= 0xFFFFFFFF
        v12 = self.ROL4(seed1, 13)

        seed2 ^= v12

        seed1 += seed3
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)
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

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)

        seed1, seed3, seed2, seed4 = self.hash_round_B1D120(seed3, seed3, seed2, seed1, seed4)

        v28 = self._keys[3]
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

        seed1, seed2, seed3, seed4 = self._to_uint32(seed1, seed2, seed3, seed4)
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

        seed1, seed2, seed3 = self._to_uint32(seed1, seed2, seed3)
        return seed1, seed2, seed3, v120

    def hash_step_40(self, seed2: int, seed3: int, seed1: int, v120: int):
        v4 = self._keys[1]
        seed2 ^= v4
        seed2 -= seed3
        seed2 &= 0xFFFFFFFF
        v8 = self.ROL4(seed3, 12)
        seed2 ^= v8
        seed1 += seed2
        seed1 &= 0xFFFFFFFF

        seed1, seed2, seed3 = self._to_uint32(seed1, seed2, seed3)

        return seed1, seed2, seed3, v120

    def hash_step_80_internal(self, seed1: int, seed3: int, v48: int, seed2: int, v120: int):
        seed1 -= seed3
        seed1 &= 0xFFFFFFFF
        seed1 ^= v48
        seed3 += seed2
        seed3 &= 0xFFFFFFFF

        seed1, seed2, seed3, v48 = self._to_uint32(seed1, seed2, seed3, v48)

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

    def _vr2_hash(self, string: bytes, seed: int):
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
        hashed = self._vr2_hash(padded, self._seed)
        hashed &= 0xFFFFFFFF
        return hashed

    def __call__(self, string: str):
        return self.hash(string)
