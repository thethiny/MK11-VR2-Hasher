import os
import sys
import json

from hashing.hash import vr2_hash
from utils import pad_string

def is_debugger_active():
    return hasattr(sys, "gettrace") and sys.gettrace() is not None

if is_debugger_active():
    os.environ.setdefault("DEBUG", "true")

if __name__ == "__main__":
    # with open("hashes_last_working.json", encoding="utf-8") as f:
    #     old_hashes = json.load(f)
    hashes = {}

    for string in [
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
    ]:
        string_padded = pad_string(string)
        hashed = vr2_hash(string_padded)
        hashes[string] = {
            "padded": string_padded,
            "hash": hashed
        }

        print(f"{string} -> {string_padded} -> {hashed}")

    # with open("hashes.json", "w", encoding="utf-8") as f:
    #     json.dump(hashes, f, ensure_ascii=False, indent=4)

    # for hash, hash_val in hashes.items():
    #     if hash_val["hash"] != old_hashes.get(hash, {"hash": ""})["hash"]:
    #         raise ValueError(f"Hash {hash} broke!")
