"""nanobind bindings for wiringPi/mcp3422.h"""



def mcp3422_setup(pin_base: int, i2c_address: int, sample_rate: int, gain: int) -> int: ...

MCP3422_SR_240: int = 0

MCP3422_SR_60: int = 1

MCP3422_SR_15: int = 2

MCP3422_SR_3_75: int = 3

MCP3422_GAIN_1: int = 0

MCP3422_GAIN_2: int = 1

MCP3422_GAIN_4: int = 2

MCP3422_GAIN_8: int = 3
