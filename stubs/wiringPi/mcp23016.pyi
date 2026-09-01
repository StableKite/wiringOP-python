"""nanobind bindings for wiringPi/mcp23016.h"""



def mcp23016_setup(pin_base: int, i2c_address: int) -> int: ...
