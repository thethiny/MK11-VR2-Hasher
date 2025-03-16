from hashing.functors import bool_functor_B1DDA0_af3b76c6
from hashing.game_consts import CONST_31FC940_POINTERS, CONST_31FC940_VALUES, CONST_31FC948
from hashing.game_internals import B1CFA0, B1D120, B1D4C0
from utils import ROL4, ROL_XOR4, print_addr, resign_seeds, test_overflow, test_overflow_def

# CLEANUP FUNCTORS
# 6
def functor_B1E1F0_62d40955(v122: int, v120: int):
    v122 = test_overflow_def(v122, "-")
    v122 = 40
    return v120, v122
# 7
def functor_B1E360_f1e25ba7(v122: int, v120: int):
    v122 = test_overflow_def(v122, "^")
    v122 = 20
    return v120, v122
# 8
def functor_B1DFC0_0b27f3fe(v122: int, v120: int):
    v122 = test_overflow_def(v122, "^")
    v122 = 0
    return v120, v122
# 9
def functor_B1E190_506be761(v122: int, v120: int):
    v122 = test_overflow_def(v122, "-")
    v122 = 60
    return v120, v122
# 10
def functor_B1DF60_000f7848(v122: int, v120: int):
    v122 = test_overflow_def(v122, "^")
    v122 = 20
    return v120, v122

# 1
def functor_B1E240_8ce1e09f(seed1: int, seed3: int, seed2: int, seed4: int, v120: int):

    print_addr_ = lambda *args: print_addr(*args, offset=0xB18000)
    seed3_ptr = seed3
    seed3_ptr = test_overflow(seed3_ptr, 296, "-")

    seed1_ptr = seed1
    seed3_ptr2 = seed3

    seed1_ptr = test_overflow(seed1_ptr, 0xA34, "+")

    seed1 += seed3_ptr2
    seed1 &= 0xFFFFFFFF
    print_addr_(0xDA6, seed1)

    seed2_ptr = seed2
    seed2_ptr = test_overflow(seed2_ptr, 0xDD2, "^")

    seed3_ptr3 = seed3
    seed2_ptr2 = seed2
    seed3_ptr3 = test_overflow(seed3_ptr3, 0xA34, "+")

    seed3 -= seed2_ptr2
    seed3 &= 0xFFFFFFFF
    print_addr_(0xE08, seed3)

    v8 = ROL4(seed2, 2)
    print_addr_(0xE17, "ROL4", v8)

    seed3_ptr4 = seed3
    seed3_ptr4 = test_overflow(seed3_ptr4, 296, "-")

    seed3 ^= v8
    print_addr_(0xE40, seed3)

    v10 = seed1
    v10 = test_overflow(v10, 296, "-")

    v11 = seed2
    v12 = seed1

    v11 = test_overflow(v11, 296, "-")

    seed2 += v12
    seed2 &= 0xFFFFFFFF
    print_addr_(0xE7A, seed2)

    seed1, seed2, seed3, seed4 = B1CFA0(seed2, seed2, seed3, seed1, seed4)
    print_addr(0xB18E99, "Functor1PostInternalCall", seed1, seed2, seed3, seed4)

    rdi = CONST_31FC940_VALUES
    rcx = CONST_31FC940_POINTERS[0]  # [rdi]
    if (CONST_31FC940_VALUES[8] - CONST_31FC940_VALUES[0]) >> 2 <= 2:
        v15 = 0
    else:
        rax = rdi[0x18]
        rcx = rcx[8]
        rcx ^= rax
        rax = CONST_31FC940_POINTERS[0x20]  # [rdi+20]
        edx = rax[rcx + 4]  # [rax+rcx+4]
        edx ^= rax[rcx]
        v15 = edx  # For Functor1, EDX is always 0x86E2354D
        # v15 = 0x86E2354D # Idk if it's for me or for everyone. Can test by checking hash during bootup.

    print_addr(0xB18ED1, v15)  # TODO: v15 is probably a seeded value
    seed2 ^= v15

    seed1 = test_overflow(seed1, 2612, "+")
    seed2 = test_overflow(seed2, 296, "-")

    seed2 -= seed1
    seed2 &= 0xFFFFFFFF

    v19 = ROL4(seed1, 14)

    seed2 = test_overflow(seed2, 0xDD2)

    seed2 ^= v19

    seed3 = test_overflow(seed3, 0xDD2)
    seed1 = test_overflow(seed1, 2612, "+")

    seed1 += seed3
    seed1 &= 0xFFFFFFFF

    print_addr(0xB18FE1, "End Of Functor Step 1", seed1, seed2, seed3, seed4)

    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)

    return seed1, seed2, seed3, seed4, v120

# 2 Internal
def functor__internal_B1E250_b7d6bccc(seed1: int, seed3: int, v48: int, seed2: int, v120: int):
    seed3 = test_overflow_def(seed3, "-")
    seed1 = test_overflow_def(seed1, "+")

    seed1 -= seed3
    seed1 &= 0xFFFFFFFF

    v48 = test_overflow_def(v48, "+")
    seed1 = test_overflow_def(seed1, "^")

    seed1 ^= v48

    seed2 = test_overflow_def(seed2, "-")
    seed3 = test_overflow_def(seed3, "^")

    seed3 += seed2
    seed3 &= 0xFFFFFFFF

    seed1, seed2, seed3, v48 = resign_seeds(seed1, seed2, seed3, v48)

    return seed1, seed2, seed3, v48, v120

# 2                         # [0]     +8          +0x18       +0x20       + 0x28     +0x30
def functor_B1E180_3d5686a6(v48: int, seed3: int, seed1: int, seed2: int, v120: int, seed4: int):
    v48 = ROL4(seed3, 4)
    if bool_functor_B1DDA0_af3b76c6(seed1, seed3):
        seed1, seed2, seed3, v48, v120 = functor__internal_B1E250_b7d6bccc(seed1, seed3, v48, seed2, v120)

    if not (CONST_31FC940_VALUES[8] - CONST_31FC940_VALUES[0]):
        v3 = 0
    else:
        v7 = CONST_31FC940_VALUES[0x18] ^ CONST_31FC940_POINTERS[0][0]
        v3 = CONST_31FC940_POINTERS[0x20][v7] ^ CONST_31FC940_POINTERS[0x20][v7 + 4]
        # Value was 0x7DF14FDC # UNSURE When I checked again it was 7DF1D6DC!

    seed1 ^= v3
    seed1 = test_overflow_def(seed1, "+")
    seed1 += 1
    seed1 &= 0xFFFFFFFF
    seed4 = seed3

    seed3, seed1, seed2, seed4 = B1D4C0(seed1, seed1, seed2, seed3, seed4) # TODO: VERIFY THAT THIS RETURN ORDER IS CORRECT

    seed1 = test_overflow_def(seed1, "^")
    seed2 = test_overflow_def(seed2, "^")

    seed2 -= seed1
    seed2 &= 0xFFFFFFFF
    v12 = ROL4(seed1, 13)

    seed2 = test_overflow_def(seed2, "^")

    seed2 ^= v12

    seed3 = test_overflow_def(seed3, "^")
    seed1 = test_overflow_def(seed1, "^")

    seed1 += seed3
    seed1 &= 0xFFFFFFFF

    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)
    return seed1, seed2, seed3, seed4, v120, v48

# 3
def functor_B1E170_20fb6053(seed3: int, seed2: int, seed1: int, seed4: int, v120: int):
    seed2 = test_overflow_def(seed2, "-")
    seed3 = test_overflow_def(seed3, "^") - seed2

    v5 = ROL_XOR4(seed2, 5) # Probably ROL again
    print_addr("X", v5)

    seed1 = test_overflow_def(seed1, "-")
    seed1 ^= v5

    seed3 = test_overflow_def(seed3, "+")
    seed2 = test_overflow_def(seed2, "+")
    seed2 += seed3
    seed2 &= 0xFFFFFFFF

    seed1 = test_overflow_def(seed1, "+")
    seed2 = test_overflow_def(seed2, "^")

    seed2 -= seed1
    seed2 &= 0xFFFFFFFF

    v13 = ROL4(seed1, 6)
    print_addr("R", v13)

    seed2 = test_overflow_def(seed2, "^")
    seed2 ^= v13

    seed3 = test_overflow_def(seed3, "-")
    seed1 = test_overflow_def(seed1, "+")
    seed1 += seed3
    seed1 &= 0xFFFFFFFF

    seed3 = test_overflow_def(seed3, "+")
    seed1 = test_overflow_def(seed1, "^")

    seed1 -= seed3
    seed1 &= 0xFFFFFFFF
    v21 = ROL4(seed3, 16)
    print_addr("R", v21)

    seed1 = test_overflow_def(seed1, "+")
    seed1 ^= v21

    seed2 = test_overflow_def(seed2, "+")

    seed3 = test_overflow_def(seed3, "^")
    seed3 += seed2
    seed3 &= 0xFFFFFFFF

    print_addr("Pre Seed", seed1, seed2, seed3, seed4)
    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)
    print_addr("Post Seed", seed1, seed2, seed3, seed4)
    seed1, seed3, seed2, seed4 = B1D120(seed3, seed3, seed2, seed1, seed4) # TODO: Game modifies memory so I need to be mindful of return order
    print_addr("Post Enter", seed1, seed2, seed3, seed4)

    if (CONST_31FC940_VALUES[8] - CONST_31FC940_VALUES[0]) >> 2 <= 3:
        v28 = 0
    else:
        v27 = CONST_31FC940_VALUES[0x18] ^ CONST_31FC940_POINTERS[0][0xC]
        v28 = CONST_31FC940_POINTERS[0x20][v27] ^ CONST_31FC940_POINTERS[0x20][v27 + 4]
        # Was 0xEAA35755 after this # This was always the same

    seed3 ^= v28

    seed2 = test_overflow_def(seed2, "+")
    seed3 = test_overflow_def(seed3, "^")

    seed3 -= seed2
    seed3 &= 0xFFFFFFFF
    v32 = ROL4(seed2, 3)

    seed3 = test_overflow_def(seed3, "^")
    seed3 ^= v32

    seed1 = test_overflow_def(seed1, "+")
    seed2 = test_overflow_def(seed2, "^")

    seed2 += seed1
    seed2 &= 0xFFFFFFFF

    seed2 = test_overflow_def(seed2, "^")
    seed3 = test_overflow_def(seed3, "+")

    seed3 -= seed2
    seed3 &= 0xFFFFFFFF
    v40 = ROL4(seed2, 4)

    seed3 = test_overflow_def(seed3, "+")
    seed3 ^= v40

    seed1 = test_overflow_def(seed1, "+")
    seed2 = test_overflow_def(seed2, "+")
    seed2 += seed1
    seed2 &= 0xFFFFFFFF

    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)
    return seed1, seed2, seed3, seed4, v120

# 4
def functor_B1E1E0_602b3a0d(seed3: int, seed2: int, seed1: int, v120: int):
    seed2 = test_overflow_def(seed2, "^")
    seed3 = test_overflow_def(seed3, "-")

    seed3 -= seed2
    seed3 &= 0xFFFFFFFF
    v5 = ROL4(seed2, 8)
    print_addr("ROL", v5)

    seed3 = test_overflow_def(seed3, "-")
    seed3 ^= v5

    seed1 = test_overflow_def(seed1, "^")
    seed2 = test_overflow_def(seed2, "^")

    seed2 += seed1
    seed2 &= 0xFFFFFFFF

    seed1 = test_overflow_def(seed1, "^")
    seed2 = test_overflow_def(seed2, "^")

    seed2 -= seed1
    seed2 &= 0xFFFFFFFF

    v13 = ROL4(seed1, 11)
    print_addr("ROL", v13)

    seed2 = test_overflow_def(seed2, "-")
    seed2 ^= v13

    seed1, seed2, seed3 = resign_seeds(seed1, seed2, seed3)
    return seed1, seed2, seed3, v120

# 5
def functor_B1E020_1e0be296(seed2, seed3, seed1, v120):
    if (CONST_31FC940_VALUES[8] - CONST_31FC940_VALUES[0]) >> 2 <= 1:
        v4 = 0
    else:
        v3 = CONST_31FC940_VALUES[0x18] ^ CONST_31FC940_POINTERS[0][4]
        v4 = CONST_31FC940_POINTERS[0x20][v3] ^ CONST_31FC940_POINTERS[0x20][v3 + 4]
        # v4 should produce a constant reproduceable value
        # v4 had in memory 0xBD3E1588
        print_addr("v4", v4)

    seed2 ^= v4

    seed3 = test_overflow_def(seed3, "-")
    seed2 = test_overflow_def(seed2, "-")

    seed2 -= seed3
    seed2 &= 0xFFFFFFFF

    v8 = ROL4(seed3, 12)
    print_addr("ROL", v8)
    seed2 = test_overflow_def(seed2, "-")

    seed2 ^= v8

    seed2 = test_overflow_def(seed2, "^")
    seed1 = test_overflow_def(seed1, "^")

    seed1 += seed2
    seed1 &= 0xFFFFFFFF

    seed1, seed2, seed3 = resign_seeds(seed1, seed2, seed3)

    return seed1, seed2, seed3, v120

if __name__ == "__main__":
    print_addr(
        "return",
        *functor_B1E170_20fb6053(0x6FD631DB, 0xFDD2992A, 0xA29311F3, 0xC9793200, 3),
    )
