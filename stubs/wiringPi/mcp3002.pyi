"""nanobind bindings for wiringPi/mcp3002.h"""



def mcp3002_setup(pin_base: int, spi_channel: int) -> int: ...
