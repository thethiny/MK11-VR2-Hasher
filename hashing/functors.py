from utils import test_overflow, sign_test_values, test_overflow_def

address_map = { # Order is important
    0xB1DC40: ("+", 0),
    0xB1DD00: ("^", 80),
    0xB1DBC0: ("-", 60),
    0xB1DF00: ("^", 20),
    0xB1DEA0: ("+", 40),
    0xB1DE00: ("^", 80),
    0xB1DD60: ("-", 60),
    0xB1DE60: ("-", 20),
    0xB1DCA0: ("+", 0),
    0xB1DC00: ("-", 40),
}

def bool_functor_B1DDA0_af3b76c6(_8: int, _16: int):
    _8 = test_overflow_def(_8, "^")
    _16 = test_overflow_def(_16, "-")
    
    return _8 > _16

def _bool_functor_(value: int, sign: str, compare: int) -> bool:
    """Performs the operation and checks the comparison."""
    test = sign_test_values.get(sign)
    if test is None:
        raise ValueError(f"Unsupported sign: {sign}")

    return test_overflow(value, test, sign) == compare

def bool_functor(lambda_address: int, loop_max: int) -> bool:
    """Selects the correct function based on the address."""
    if lambda_address in address_map:
        sign, compare = address_map[lambda_address]
        return _bool_functor_(loop_max, sign, compare)
    raise ValueError(f"Unsupported Bool Functor {lambda_address}")