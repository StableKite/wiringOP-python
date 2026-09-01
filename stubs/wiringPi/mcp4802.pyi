"""nanobind bindings for wiringPi/mcp4802.h"""



def mcp4802_setup(pin_base: int, spi_channel: int) -> int: ...
