def generate_keys_from_string(encryption_string: bytes):
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
            v11 = 0 # index into encryption string
            v4 = v10 + 1
            if not v10:
                v4 = 0
            v6 = v4
            v3 = b""
            if v4:
                v3 = encryption_string[v11 + v8 +1: v11 + v8 + v10 +1] # Copy specific bytes from
            v12 = v3
            if not v4:
                v12 = b"" # Null
        else:
            v12 = b""
    else:
        v12 = b""

    # LABEL_15
    v13 = v12[8]
    v14 = v12[4]
    v15 = v12[0]

    v16 = complex_op(
        v12, 0, 0x9FD33AE8, 0x1169237E, 0x70263B48, 0x9FD33A, 0x11, 0x1169
    )

    v17 = b""
    if v6:
        v17 = v3
    v44 = complex_op(v17, 1, 0x3B9FA118, 3756927701, -0x7720C8E, 0x3B9FA1, 0x11, 0xDFEE)

    v21 = b""
    if v4:
        v21 = v3
    v25 = complex_op(v21, 2, -538039595, 0xE7026B48, 0x9C1BF55D, 0xDFEE2A, 17, 0xE702)

    v26 = b""
    if v4:
        v26 = v3

    v30 = complex_op(v26, 3, -0x18FD94B8, 0xDFEE2AD5, 0x29C08DAF, 0xE7026B, 0x11, 0xDFEE)
    v28 = v26[3+4]

    v31 = v16 ^ v44
    v32 = v25 ^ v44
    v33 = v25 ^ v30
    v45 = v31 ^ v30

    key_1 = v31 ^ 0x77E56F3D
    key_2 = v32 ^ 0x250A0D57
    key_3 = v33 ^ 0xA4CA9627
    key_4 = v45 ^ 0x9414718A
    
    return key_1, key_2, key_3, key_4
    # _mul = (0x18FD94B8 * v28) & 0xFFFFFFFF
    # v33 = v25 ^ ((v30 - _mul) & 0xFFFFFFFF)
    # v45 = v31 ^ ((v30 - _mul) & 0xFFFFFFFF)

    # v34 = xor_seeds_array # the one with size 2 Million
    # rcx = xor_key
    # edx = xor_seeds_array[0]
    # edx ^= rcx # becomes index
    # eax = xors_arr[rcx] # index +1
    # eax ^= v31
    # eax ^= 0x77e56f3d


def complex_op(string, offset, mul_2, mul_1, mul_3, add_2, add_3, add_1):
    v13 = string[8+offset]
    v14 = string[4+offset]
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

if __name__ == "__main__":
    keys = generate_keys_from_string(string)
    print(list(hex(a) for a in keys))
