"""nanobind bindings for wiringPi/drcSerial.h"""



def drc_setup_serial(pin_base: int, num_pins: int, device: str, baud: int) -> int: ...
