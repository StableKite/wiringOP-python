import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.ds1302")

def test_ds1302rtc_read():
    _=m.ds1302rtc_read(1)

def test_ds1302rtc_write():
    _=m.ds1302rtc_write(1, 1)

def test_ds1302ram_read():
    _=m.ds1302ram_read(1)

def test_ds1302ram_write():
    _=m.ds1302ram_write(1, 1)

def test_ds1302_clock_read():
    assert m.ds1302_clock_read()==tuple(range(10,18))

def test_ds1302_clock_write():
    m.ds1302_clock_write(range(8))
    with pytest.raises(ValueError):m.ds1302_clock_write([1])

def test_ds1302trickle_charge():
    _=m.ds1302trickle_charge(1, 1)

def test_ds1302setup():
    _=m.ds1302setup(1, 1, 1)
