"""nanobind bindings for wiringPi/mcp23s17.h"""



def mcp23s17_setup(pin_base: int, spi_port: int, dev_id: int) -> int: ...
