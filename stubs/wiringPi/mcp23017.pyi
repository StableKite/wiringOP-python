"""nanobind bindings for wiringPi/mcp23017.h"""



def mcp23017_setup(pin_base: int, i2c_address: int) -> int: ...
