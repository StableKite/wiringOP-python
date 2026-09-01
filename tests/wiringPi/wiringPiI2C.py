import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wiring_pi_i2c")

def test_wiring_pi_i2c_read():
    _=m.wiring_pi_i2c_read(1)

def test_wiring_pi_i2c_read_reg8():
    _=m.wiring_pi_i2c_read_reg8(1, 1)

def test_wiring_pi_i2c_read_reg16():
    _=m.wiring_pi_i2c_read_reg16(1, 1)

def test_wiring_pi_i2c_write():
    _=m.wiring_pi_i2c_write(1, 1)

def test_wiring_pi_i2c_write_reg8():
    _=m.wiring_pi_i2c_write_reg8(1, 1, 1)

def test_wiring_pi_i2c_write_reg16():
    _=m.wiring_pi_i2c_write_reg16(1, 1, 1)

def test_wiring_pi_i2c_setup_interface():
    _=m.wiring_pi_i2c_setup_interface("x", 1)

def test_wiring_pi_i2c_setup():
    _=m.wiring_pi_i2c_setup(1)
