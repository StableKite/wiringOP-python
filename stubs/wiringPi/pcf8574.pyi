"""nanobind bindings for wiringPi/pcf8574.h"""



def pcf8574_setup(pin_base: int, i2c_address: int) -> int: ...
