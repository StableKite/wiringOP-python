"""nanobind bindings for wiringPi/pcf8591.h"""



def pcf8591_setup(pin_base: int, i2c_address: int) -> int: ...
