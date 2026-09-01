import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wiring_pi_spi")

def test_wiring_pi_spi_get_fd():
    _=m.wiring_pi_spi_get_fd(1)

def test_wiring_pi_spi_data_rw():
    b=bytearray([1,2,3]);assert m.wiring_pi_spi_data_rw(0,b)==3;assert b==bytearray([0xA4,0xA7,0xA6])
    with pytest.raises((TypeError,BufferError)):m.wiring_pi_spi_data_rw(0,b"abc")

def test_wiring_pi_spi_setup_mode():
    _=m.wiring_pi_spi_setup_mode(1, 1, 1, 1)

def test_wiring_pi_spi_setup():
    _=m.wiring_pi_spi_setup(1, 1)
