"""nanobind bindings for wiringPi/ads1115.h"""



def ads1115_setup(pin_base: int, i2c_address: int) -> int: ...

ADS1115_GAIN_6: int = 0

ADS1115_GAIN_4: int = 1

ADS1115_GAIN_2: int = 2

ADS1115_GAIN_1: int = 3

ADS1115_GAIN_HALF: int = 4

ADS1115_GAIN_QUARTER: int = 5

ADS1115_DR_8: int = 0

ADS1115_DR_16: int = 1

ADS1115_DR_32: int = 2

ADS1115_DR_64: int = 3

ADS1115_DR_128: int = 4

ADS1115_DR_250: int = 5

ADS1115_DR_475: int = 6

ADS1115_DR_860: int = 7
