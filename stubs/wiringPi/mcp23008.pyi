"""nanobind bindings for wiringPi/mcp23008.h"""



def mcp23008_setup(pin_base: int, i2c_address: int) -> int: ...
