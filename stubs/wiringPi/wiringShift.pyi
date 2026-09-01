"""nanobind bindings for wiringPi/wiringShift.h"""



def shift_in(d_pin: int, c_pin: int, order: int) -> int: ...

def shift_out(d_pin: int, c_pin: int, order: int, val: int) -> None: ...

LSBFIRST: int = 0

MSBFIRST: int = 1
