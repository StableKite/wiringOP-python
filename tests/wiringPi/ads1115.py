import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.ads1115")

def test_ads1115_setup():
    _=m.ads1115_setup(1, 1)

def test_constants_and_macros():
    assert hasattr(m,"ADS1115_GAIN_6")
    assert hasattr(m,"ADS1115_GAIN_4")
    assert hasattr(m,"ADS1115_GAIN_2")
    assert hasattr(m,"ADS1115_GAIN_1")
    assert hasattr(m,"ADS1115_GAIN_HALF")
    assert hasattr(m,"ADS1115_GAIN_QUARTER")
    assert hasattr(m,"ADS1115_DR_8")
    assert hasattr(m,"ADS1115_DR_16")
    assert hasattr(m,"ADS1115_DR_32")
    assert hasattr(m,"ADS1115_DR_64")
    assert hasattr(m,"ADS1115_DR_128")
    assert hasattr(m,"ADS1115_DR_250")
    assert hasattr(m,"ADS1115_DR_475")
    assert hasattr(m,"ADS1115_DR_860")
