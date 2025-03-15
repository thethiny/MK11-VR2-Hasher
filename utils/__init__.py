import os
import struct
from typing import Union
try:
    import pymem
    PYMEM_ENABLED = True
except ImportError:
    PYMEM_ENABLED = False

def ROL4(value, shift):
    value &= 0xFFFFFFFF
    l = (value << shift) & 0xFFFFFFFF
    r = (value >> (32 - shift)) & 0xFFFFFFFF
    return l | r

def ROL_XOR4(value, shift):
    value &= 0xFFFFFFFF
    l = (value << shift) & 0xFFFFFFFF
    r = (value >> shift) & 0xFFFFFFFF
    return l ^ r


def print_exit(*args, **kwargs):
    print(*args, **kwargs)
    exit()

def print_addr(addr: Union[int, str], *args, offset: int = 0):
    if os.environ.get("DEBUG", False) not in ["true", "True", True, 1, "1"]:
        return
        
    args_f = []
    for arg in args:
        if isinstance(arg, int):
            if arg >= 0x100000000:
                arg = f"{arg:0>16X}"
            else:
                arg = f"{arg:0>8X}"
        args_f.append(arg)
    if isinstance(addr, int):
        addr += offset
        print(f"MK11.exe+{addr:0>6X}:", *args_f)
    else:
        print(f"{addr: >15}:", *args_f)


def combine_bytes(value_size: int, *values):
    format_map = {1: "B", 2: "H", 4: "I", 8: "Q", 16: "16s"}
    format_string = f"<{len(values)}{format_map[value_size]}"  # "<" = little-endian

    packed_data = struct.pack(format_string, *values)
    return packed_data


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

def test_overflow(value: int, add_value: int, op: str = "+", size=4, ):
    mask = get_bitmask_ff(size)

    if op == "+":
        value += add_value
    if op == "-":
        value -= add_value
    if op == "^":
        value ^= add_value
    value &= mask  # Apply size-based masking

    if op == "+":
        value -= add_value
    if op == "^":
        value ^= add_value
    if op == "-":
        value += add_value
    value &= mask  # Apply size-based masking again

    return value

# Define fixed test values for each sign
sign_test_values = {
    "+": 0xA34,
    "-": 0x128,
    "^": 0xDD2,
}

def test_overflow_def(value: int, op: str, size: int = 4):
    add_value = sign_test_values.get(op)
    if add_value is None:
        raise ValueError(f"Passed invalid operation `{op}`")
    
    return test_overflow(value, add_value, op, size)

def magic_division(value, magic, extra_shift=0):
    # Multiply, keep the high 64 bits, then shift, then sign-correct.
    prod = value * magic
    hi = prod >> 64
    return (hi >> extra_shift) + (hi >> 63)


def resign_seeds(*seeds: int, size: int = 4):
    mask = get_bitmask_ff(size)
    inputs = [a&mask for a in seeds]
    return inputs

PAD_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def pad_string(string: str, pad_length: int = 12) -> str:
    if len(string) % pad_length != 0:
        return string + PAD_ALPHA[: pad_length - (len(string) % pad_length)]

    return string

def dump(*arrays: Union[bytearray, bytes], name: str):
    if not name.lower().endswith(".bin"):
        name += ".bin"
    array = bytearray()
    for a in arrays:
        array += a
    with open(name, "wb") as f:
        f.write(array)

if PYMEM_ENABLED:
    def dump_memory(process_name, address, length, filename=None):
        try:
            pm = pymem.Pymem(process_name)
            data = pm.read_bytes(address, length)

            if filename is None:
                filename = f"{process_name}_{hex(address)}-{hex(length)}.bin"

            dump(data, name=filename)
            print(f"Memory dumped to {filename}")

        except Exception as e:
            print(f"Error: {e}")


    def compare_memory(expected_bytes, process_address, process_name: str = "mk11.exe", all=False):
        try:
            pm = pymem.Pymem(process_name)
            actual_bytes = pm.read_bytes(process_address, len(expected_bytes))

            # Size check
            if len(actual_bytes) != len(expected_bytes):
                print(
                    f"Size mismatch: Expected {len(expected_bytes)}, Found {len(actual_bytes)}"
                )
                if len(actual_bytes) > len(expected_bytes):
                    print("Memory is bigger than expected.")
                else:
                    print("Memory is smaller than expected.")
                return

            # Compare bytes
            mismatches = []
            start = None
            for i, (exp, act) in enumerate(zip(expected_bytes, actual_bytes)):
                if exp != act:
                    if start is None:
                        start = i
                else:
                    if start is not None:
                        mismatches.append((start, i - 1))
                        if not all:
                            print(f"Mismatch at bytes {start}-{i - 1}")
                            return
                        start = None

            if start is not None:
                mismatches.append((start, len(expected_bytes) - 1))

            if mismatches:
                for start, end in mismatches:
                    print(f"Mismatch at bytes {start}-{end}")
            else:
                print("Memory contents are identical.")

        except Exception as e:
            print(f"Error: {e}")
