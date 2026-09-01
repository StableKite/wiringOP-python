"""nanobind bindings for wiringPi/mcp23s08.h"""



def mcp23s08_setup(pin_base: int, spi_port: int, dev_id: int) -> int: ...
