from hashing.game_consts import CONST_31FC940_POINTERS, CONST_31FC940_VALUES
from proper.Hasher import VR2Hasher

if __name__ == "__main__":
    # make
    xor_key = CONST_31FC940_VALUES[0x18]
    key_1 = CONST_31FC940_POINTERS[0][0] ^ xor_key
    key_2 = CONST_31FC940_POINTERS[0][4] ^ xor_key
    key_3 = CONST_31FC940_POINTERS[0][8] ^ xor_key
    key_4 = CONST_31FC940_POINTERS[0][12] ^ xor_key

    keys = []
    for key in [key_1, key_2, key_3, key_4]:
        key = CONST_31FC940_POINTERS[0x20][key] ^ CONST_31FC940_POINTERS[0x20][key+4]
        keys.append(key)

    print([hex(a) for a in keys])

    hasher = VR2Hasher(*keys, hash_seed=0x291)

    strings = [
        "",
        "1",
        "test23",
        "thethiny",
        "12345678901234567890123",
        "12345678901234567890123A",
        "12345678901234567890123B",
        "123456789012345678901231",
        "123456789012345678901232",
        "123456789012345678901233",
        "123456789012345678901234",
        "wesrxdctfvgy987yasd8y79g18y7wh78d871h287d1nb8ashd78ygb6t7y12vf7e1",
        "wesrxdctfvgy987yasd8y79g18y7wh78d871h287d1nb8ashd78ygb6t7y12vf7e1ABCDEFG",
        "765F6G768yu7g76gx76O899H87OH9h98787F65d54654665f65F65f675F665F65f65f65ftjhGLgflGLlgGl",
        "765F6G768yu7g76gx76O899H87OH9h98787F65d54654665f65F65f675F665F65f65f65ftjhGLgflGLlgGl765F6G768yu7g76gx76O899H87OH9h98787F65d54654665f65F65f675F665F65f65f65ftjhGLgflGLlgGl765F6G768yu7g76gx76O899H87OH9h98787F65d54654665f65F65f675F665F65f65f65ftjhGLgflGLlgGl",
    ]

    for string in strings:
        print(string, "->", hasher.hash(string))
