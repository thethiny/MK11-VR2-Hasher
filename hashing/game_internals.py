from hashing.game_consts import ADE9B0, CONST_31FA270
from utils import ROL4, magic_division, print_addr, resign_seeds, test_overflow


def B1CFA0(seed2_copy: int, seed2: int, seed3: int, seed1: int, seed4: int):  # REMADE
    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)

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
    print_addr(0xB1D0F, seed1, seed2, seed3, seed4)

    if (seed2_copy % 678) > 31:  # USED
        v10 = ADE9B0()
        seed1, seed2, seed3, seed4 = B1D4C0(
            seed2_copy // v10 - 3, seed2, seed3, seed1, seed4
        )

    if (seed2_copy % 7) < 3:
        division_result = magic_division(seed2_copy, 0x6666666666666667, 1)
        seed1, seed2, seed3, seed4 = B1D120(
            division_result - 6, seed2, seed3, seed1, seed4
        )

    if (seed2_copy % 11) > 4:
        seed1, seed2, seed3, seed4 = B1D280(
            seed2_copy // 7 - 6, seed2, seed3, seed1, seed4
        )

    return seed1, seed2, seed3, seed4


def B1D4C0(seed2_copy, seed2, seed3, seed1, seed4):  # REMADE
    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)
    print_addr(0xB1D4C0, seed2_copy, seed1, seed2, seed3, seed4)

    if seed2_copy <= 0:
        return seed1, seed2, seed3, seed4

    seed2 = test_overflow(seed2, 296, "-")
    seed3 = test_overflow(seed3, 2612, "+")

    seed3 -= seed2
    seed3 &= 0xFFFFFFFF

    v9 = ROL4(seed2, 3)

    seed3 = test_overflow(seed3, 296, "-")

    seed3 ^= v9

    seed1 = test_overflow(seed1, 2612, "+")
    seed2 = test_overflow(seed2, 2612, "+")

    seed2 += seed1
    seed2 &= 0xFFFFFFFF

    seed3 = test_overflow(seed3, 2612, "+")
    seed1 = test_overflow(seed1, 2612, "+")

    seed1 -= seed3
    seed1 &= 0xFFFFFFFF

    v10 = ROL4(seed3, 2)

    seed2 = test_overflow(seed2, 296, "-")

    seed2 ^= v10

    seed1 = test_overflow(seed1, 2612, "+")
    seed3 = test_overflow(seed3, 0xDD2, "^")

    seed3 += seed1
    seed3 &= 0xFFFFFFFF
    seed4 += 9
    seed4 &= 0xFFFFFFFF
    seed2 ^= seed4

    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)

    print_addr(0xB1D669, seed1, seed2, seed3, seed4)

    if (
        seed2_copy % 4 == 0
    ):  # ORIGIN COND if ( ((((seed2 >> 63) & 3) + (_DWORD)seed2) & 3) == ((seed2 >> 63) & 3) )
        division_result = magic_division(seed2_copy, 0x4924924924924925, 1)
        seed1, seed2, seed3, seed4 = B1CFA0(
            division_result - 3, seed2, seed3, seed1, seed4
        )

    if (seed2_copy % 5) < 3:  # USED
        div_result = seed2_copy // 4
        seed1, seed2, seed3, seed4 = B1D120(
            div_result - 6, seed2, seed3, seed1, seed4
        )  # IT WENT WRONG SOMEWHERE INSIDE HERE :(

    if (seed2_copy % 8) > 4:  # USED
        div_result = magic_division(seed2_copy, 0x5555555555555556)
        seed1, seed2, seed3, seed4 = B1D280(div_result - 6, seed2, seed3, seed1, seed4)

    return seed1, seed2, seed3, seed4


def B1D120(seed2_copy, seed2, seed3, seed1, seed4):  # REMADE
    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)

    if seed2_copy <= 0:
        return seed1, seed2, seed3, seed4

    seed2 -= seed3
    seed2 &= 0xFFFFFFFF
    seed1 ^= (seed3 << 7) ^ ((seed3 & 0xFFFFFFFF) >> 7)
    seed1 += seed3
    seed1 &= 0xFFFFFFFF
    seed4 *= 5
    seed4 &= 0xFFFFFFFF

    print_addr(0xB1D17D, seed1, seed2, seed3, seed4)

    if (seed2_copy & 1) == 0:  # USED
        div_result = magic_division(seed2_copy, 0x5555555555555556)
        seed1, seed2, seed3, seed4 = B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
    if (seed2_copy % 7) < 3:  # USED
        div_result = magic_division(seed2_copy, 0x6666666666666667, 1)
        seed1, seed2, seed3, seed4 = B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
    if (seed2_copy % 11) > 4:  # USED
        div_result = seed2_copy // 7
        seed1, seed2, seed3, seed4 = B1D280(div_result - 6, seed2, seed3, seed1, seed4)

    return seed1, seed2, seed3, seed4


def B1D280(seed2_copy, seed2, seed3, seed1, seed4):  # REMADE
    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)

    if seed2_copy <= 0:
        return seed1, seed2, seed3, seed4

    seed1 = test_overflow(seed1, 2612, "+")
    seed2 = test_overflow(seed2, 2612, "+")

    seed2 -= seed1
    seed2 &= 0xFFFFFFFF

    v9 = ROL4(seed1, 2)

    seed2 = test_overflow(seed2, 0xDD2)

    seed2 ^= v9

    seed3 = test_overflow(seed3, 0xDD2)
    seed2 = test_overflow(seed2, 0xDD2)

    seed2 += seed3
    seed2 &= 0xFFFFFFFF

    seed4 *= 8
    seed4 &= 0xFFFFFFFF
    seed2 ^= seed4

    seed1, seed2, seed3, seed4 = resign_seeds(seed1, seed2, seed3, seed4)
    print_addr(0xB1D38B, seed1, seed2, seed3, seed4)

    if (seed2_copy % 7) > 3:  # USED
        div_result = magic_division(seed2_copy, 0x4924924924924925, 2)
        seed1, seed2, seed3, seed4 = B1D4C0(div_result - 3, seed2, seed3, seed1, seed4)
    if (seed2_copy % 9) < 2:
        div_result = magic_division(seed2_copy, 0x5555555555555556)
        seed1, seed2, seed3, seed4 = B1CFA0(div_result - 6, seed2, seed3, seed1, seed4)
    if (seed2_copy % 131) > 66:  # USED
        div_result = magic_division(seed2_copy, 0x6666666666666667, 1)
        seed1, seed2, seed3, seed4 = B1D280(div_result - 7, seed2, seed3, seed1, seed4)

    return seed1, seed2, seed3, seed4
