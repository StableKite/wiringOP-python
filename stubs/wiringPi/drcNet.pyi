"""nanobind bindings for wiringPi/drcNet.h"""



def drc_setup_net(pin_base: int, num_pins: int, ip_address: str, port: str, password: str) -> int: ...
