from typing import Union
from hashing.step_functors import (
    functor_B1DF60_000f7848,
    functor_B1DFC0_0b27f3fe,
    functor_B1E020_1e0be296,
    functor_B1E170_20fb6053,
    functor_B1E180_3d5686a6,
    functor_B1E190_506be761,
    functor_B1E1E0_602b3a0d,
    functor_B1E1F0_62d40955,
    functor_B1E240_8ce1e09f,
    functor_B1E360_f1e25ba7,
)
from utils import print_addr, str_to_bytes
from hashing.functors import bool_functor

# Seed 4 always ends up being a copy of seed3 +- some small value
def vr2_inner_hash(thread_id: int, active_thread_id: int, seed1: int, seed2: int, seed3: int, seed4: int):
    v120 = 3
    v48 = 0
    v122 = 23

    if active_thread_id != thread_id:
        raise ValueError(f"Called Thread {thread_id} outside its proper order! Expected thread {active_thread_id}")

    functor_result = bool_functor(0xB1DC40, active_thread_id) # 5268d16c
    if functor_result:
        seed1, seed2, seed3, seed4, v120 = functor_B1E240_8ce1e09f(seed1, seed3, seed2, seed4, v120)
        print_addr("Functor1 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DD00, active_thread_id) # 8c1c78cb
    if functor_result:
        seed1, seed2, seed3, seed4, v120, v48 = functor_B1E180_3d5686a6(v48, seed3, seed1, seed2, v120, seed4)
        print_addr("Functor2 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DBC0, active_thread_id) # 025ccbb2
    if functor_result:
        seed1, seed2, seed3, seed4, v120 = functor_B1E170_20fb6053(seed3, seed2, seed1, seed4, v120)
        print_addr("Functor3 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DF00, active_thread_id) # f4fd335e
    if functor_result:
        seed1, seed2, seed3, v120 = functor_B1E1E0_602b3a0d(seed3, seed2, seed1, v120)
        print_addr("Functor4 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DEA0, active_thread_id) # f477e9d7
    if functor_result:
        seed1, seed2, seed3, v120 = functor_B1E020_1e0be296(seed2, seed3, seed1, v120)
        print_addr("Functor5 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DE00, active_thread_id) # c023a3a6
    if functor_result:
        v120, v122 = functor_B1E1F0_62d40955(v122, v120)
        print_addr("Functor6 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DD60, active_thread_id) # ab18cd68
    if functor_result:
        v120, v122 = functor_B1E360_f1e25ba7(v122, v120)
        print_addr("Functor7 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DE60, active_thread_id) # f0e81d38
    if functor_result:
        v120, v122 = functor_B1DFC0_0b27f3fe(v122, v120)
        print_addr("Functor8 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DCA0, active_thread_id) # 5d1274b1
    if functor_result:
        v120, v122 = functor_B1E190_506be761(v122, v120)  # <- Enter here
        print_addr("Functor9 Out", seed1, seed2, seed3, seed4)

    functor_result = bool_functor(0xB1DC00, active_thread_id) # 0e53aea5
    if functor_result:
        v120, v122 = functor_B1DF60_000f7848(v122, v120)
        print_addr("Functor10 Out", seed1, seed2, seed3, seed4)

    active_thread_id = v122
    return active_thread_id, seed1, seed2, seed3, seed4


def vr2_hash(string: Union[str, bytes], seed: int = 0x291):
    if isinstance(string, str):
        string = string.encode("ascii")

    string_length = len(string)

    thread_id = seed3_v74 = seed_4v44 = total_read_string_bytes = 0
    v9 = ((seed - 1) | 0x80000000) + (
        4 * string_length
    )
    seed3_v74 = v10 = seed2_v41 = v11 = seed1_v40 = v9
    print_addr(0xB1BD45, v9)

    if string_length >= 0x0C:
        string_seeder_offset = 8  # int
        while 2:
            seed2_v41 = str_to_bytes(string, string_seeder_offset - 4) + v10 # TODO: NEEDS TO MASK
            seed2_v41 &= 0xFFFFFFFF
            print_addr(0xB1BD84, "v41", seed2_v41)

            v14 = str_to_bytes(string, string_seeder_offset) + v9
            v14 &= 0xFFFFFFFF
            print_addr(0xB1BD94, "v14", v14)

            temp = v14 << 4
            temp &= 0xFFFFFFFF  # Enforce 32b
            print_addr(0xB1BD97, temp)
            temp2 = v14 >> 28
            print_addr(0xB1BDA0, temp2)
            left_side = temp2 | temp
            print_addr(0xB1BDA3, left_side)
            left_side &= 0xFFFFFFFF

            right_side = str_to_bytes(string, total_read_string_bytes) + v11 - v14
            right_side &= 0xFFFFFFFF
            print_addr(0xB1BDAA, right_side)

            seed1_v40 = left_side ^ right_side
            print_addr(0xB1BDB2, "v40", seed1_v40)

            seed3_v74 = (seed2_v41 + v14) & 0xFFFFFFFF
            print_addr(0xB1BDB6, "v74", seed3_v74)

            active_thread_id = 80  # 0x50
            thread_id = 20
            print_addr(f"Starting Thread =", active_thread_id)

            for _ in range(5):
                thread_id = active_thread_id
                print_addr(f"Thread Id {thread_id}: Seeds", seed1_v40, seed2_v41, seed3_v74, "some_counter:", seed_4v44)
                active_thread_id, seed1_v40, seed2_v41, seed3_v74, seed_4v44 = (
                    vr2_inner_hash(thread_id, active_thread_id, seed1_v40, seed2_v41, seed3_v74, seed_4v44)
                )
                thread_id += 20 # Kept for compatibility, can remove but you have to remove internal raise

            string_seeder_offset += 12 # Length
            total_read_string_bytes += 12 # Why?
            print_addr(f"while loop {string_seeder_offset=}", total_read_string_bytes, string_seeder_offset, string_seeder_offset + 4, string_length)

            if string_seeder_offset + 4 <= string_length:
                v11 = seed1_v40
                v10 = seed2_v41
                v9 = seed3_v74
                continue

            break

    return hex(seed3_v74)
