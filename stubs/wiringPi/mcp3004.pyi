"""nanobind bindings for wiringPi/mcp3004.h"""



def mcp3004_setup(pin_base: int, spi_channel: int) -> int: ...
