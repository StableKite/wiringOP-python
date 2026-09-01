"""nanobind bindings for wiringPi/sr595.h"""



def sr595_setup(pin_base: int, num_pins: int, data_pin: int, clock_pin: int, latch_pin: int) -> int: ...
