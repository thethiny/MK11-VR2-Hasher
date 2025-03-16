from utils import print_addr

CONST_31FA274 = 0xA3A1E1BC  # Something is resetting this back after moving it
CONST_31FA270 = 3  # Something is resetting this back after moving it
# TODO: REPLACE THESE VALUES
CONST_31FC948 = 0x139DD  # IDK too # UNUSED
# TODO: These values all changed, but the output seed remained the same!
CONST_31FC940_VALUES = {
    0x0: 0x2585246C550,  # Pointer to some seeding values
    0x8: 0x2585246C560,  # Pointer to previous hash
    0x10: 0x2585246C560,  # Pointer to previous hash
    0x18: 0xC1220A4F,  # 1st time 0x1D151DED,  # Value # 2nd time it was C1220A4F # custom seed was 2246651937
    # 0x1C: 0x64697272, # Useless data
    0x20: 0x25853874CE0,  # Random Bytes Array # Used for seeding maybe? I noticed that this is different every run so I'm unsure how the hash is the same
    0x28: 2000000,  # Random Bytes Size
    0x2C: 0,
}
CONST_31FC940_POINTERS = {
    0x0: {
        0x00: 0xC12DD270,  # First Time 0x1D05C9BA, # 2nd time it was 0xC12DD270 # Custom seed was 2247883720
        0x04: 0xC127CE59,  # First Time 0x1D1F0286, # 2nd time it was C127CE59  # Custom seed was 2248031539
        0x08: 0xC12961C7,  # First Time 0x1D020ED5, # 2nd time it was C12961C7  # Custom seed was 2246879723
        0x0C: 0xC136C938,  # First Time 0x1D10B785, # 2nd Time it was C136C938  # Custom seed was 2246434811
    },
    0x20: {
        0x171338: 0xA7D00BAA,  # 1st time it changed and address changed
        0x17133C: 0x21323EE7,  # 1st time it changed and address changed
        0x0B6B88: 0x146C88CF,  # 2nd time it changed and address changed
        0x0B6B8C: 0x928EBD82,  # 2nd time it changed and address changed
        0x05C416: 0x6C63BF6F,
        0x05C41A: 0xD15DAAE7,
        0x14C377: 0x500B7FCC,
        0x14C37B: 0xBAA82899,
        0x0FD83F: 0xF3A531EE,
        0x0FD843: 0x8E54E732,
        # Custom Seeds
        1231849: 4068612868,
        1231853: 2407823303,
        1510674: 2351425458,
        1510678: 3501585905,
        367050: 1254869655,
        367054: 3050537601,
        847834: 3608359765,
        847838: 2286300682,
    },
}


def ADE9B0():
    global CONST_31FA274

    v0 = CONST_31FA270  # This value may be the seed or something that changes per account, debug! Exists at 0x31FA274 # Update, yes it does change per value
    for i in range(0, 100, 2):
        v2 = i * v0
        v2 &= 0xFFFFFFFF
        v3 = i + 1
        v3 &= 0xFFFFFFFF
        v0 = v3 * (v2 + 20) + 20
        v0 &= 0xFFFFFFFF

    CONST_31FA274 = v0
    print_addr(0x31FA274, "CONST", CONST_31FA274)

    # CONST ALWAYS ENDS UP BEING THE SAME THEREFORE INITIAL VALUE IS MEANINGLESS!
    # YOU CAN REPLACE THE FUNCTION WITH CONST274 = A7AC5CC0 AND THEN RETURN THE OTHER CONST

    return CONST_31FA270
